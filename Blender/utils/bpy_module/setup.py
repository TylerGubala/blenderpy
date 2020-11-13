#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Build blender into a python module
"""

from distutils.command.install_data import install_data
import os
import pathlib
import re
from setuptools import find_packages, setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install
from setuptools.command.install_lib import install_lib
from setuptools.command.install_scripts import install_scripts
import shutil
import sys
from typing import List, Set

class CMakeExtension(Extension):
    """
    An extension to run the cmake build
    """

    def __init__(self, name, sources=[]):

        super().__init__(name = name, sources = sources)

class InstallCMakeLibsData(install_data):
    """
    Just a wrapper to get the install data into the egg-info
    """

    def run(self):
        """
        Outfiles are the libraries that were built using cmake
        """

        # Mark libraries for distribution explicitly

        self.outfiles = self.distribution.data_files

class InstallCMakeLibs(install_lib):
    """
    Get the libraries from the parent distribution, use those as the outfiles

    Skip building anything; everything is already built, forward libraries to
    the installation step
    """

    def run(self):
        """
        Copy libraries from the bin directory and place them as appropriate
        """

        self.announce("Moving library files", level=3)

        # We have already built the libraries in the previous build_ext step

        self.skip_build = True

        bin_dir = self.distribution.bin_dir

        libs = [os.path.join(bin_dir, _lib) for _lib in 
                os.listdir(bin_dir) if 
                os.path.isfile(os.path.join(bin_dir, _lib)) and 
                os.path.splitext(_lib)[1] in [".dll", ".so"]
                and not (_lib.startswith("python") or _lib.startswith("bpy"))]

        for lib in libs:

            shutil.move(lib, os.path.join(self.build_dir,
                                          os.path.basename(lib)))

        # Mark the libs for installation, adding them to 
        # distribution.data_files seems to ensure that setuptools' record 
        # writer appends them to installed-files.txt in the package's egg-info

        self.distribution.data_files = [os.path.join(self.install_dir, 
                                                     os.path.basename(lib))
                                        for lib in libs]

        # Must be forced to run after adding the libs to data_files

        self.distribution.run_command("install_data")

        super().run()

class InstallBlenderScripts(install_scripts):
    """
    Install the scripts available from the "version folder" in the build dir
    """

    def run(self):
        """
        Copy the required directory to the build directory and super().run()
        """

        self.announce("Moving scripts files", level=3)

        self.skip_build = True

        bin_dir = self.distribution.bin_dir

        scripts_dirs = [os.path.join(bin_dir, _dir) for _dir in
                        os.listdir(bin_dir) if
                        os.path.isdir(os.path.join(bin_dir, _dir))]

        for scripts_dir in scripts_dirs:

            dst_dir = os.path.join(self.build_dir,
                                   os.path.basename(scripts_dir))

            # Mostly in case of weird things happening during build
            if os.path.exists(dst_dir):
                
                if os.path.isdir(dst_dir): 

                    shutil.rmtree(dst_dir)

                elif os.path.isfile(dst_dir):

                    os.remove(dst_dir)

            shutil.copytree(scripts_dir,
                            os.path.join(self.build_dir,
                                         os.path.basename(scripts_dir)))

        # Mark the scripts for installation, adding them to 
        # distribution.scripts seems to ensure that the setuptools' record 
        # writer appends them to installed-files.txt in the package's egg-info

        self.distribution.scripts = scripts_dirs

        super().run()

class BuildCMakeExt(build_ext):
    """
    Uses prebuilt cmake instead of the python setuptools implicit build
    """

    def run(self):
        """
        Perform copy_bpy before doing the 'normal' stuff
        """

        os.makedirs(str(pathlib.Path(self.build_temp).absolute()), 
                    exist_ok=True)

        for extension in self.extensions:

            extension_path = pathlib.Path(self.get_ext_fullpath(extension.name))

            if isinstance(extension,CMakeExtension):

                self.announce(f"Preparing the build environment for CMake "
                              f"extension: \"{extension.name}\"", level=3)

                os.makedirs(str(extension_path.parent.absolute()),
                            exist_ok=True)

            if extension.name == "bpy":

                search_dir = pathlib.Path(__file__).parent.absolute()

                self.copy_bpy(search_dir, extension_path)

        super().run()

    def copy_bpy(self, source_path: pathlib.Path, dest_path: pathlib.Path):
        """
        Move the bpy files
        """

        self.announce("Searching for Blender python module", level=3)

        bpy_canidates = [os.path.join(source_path, _bpy) for _bpy in
                         os.listdir(source_path) if
                         os.path.isfile(os.path.join(source_path, _bpy)) and
                         os.path.splitext(_bpy)[0].startswith('bpy') and
                         os.path.splitext(_bpy)[1] in [".pyd", ".so"]]

        if not bpy_canidates:

            raise Exception(f"Could not find Blender python module in {source_path}")

        bpy_path = bpy_canidates[0]
            
        self.distribution.bin_dir = source_path

        self.announce("Moving Blender python module", level=3)

        shutil.copy(str(bpy_path), str(dest_path))

        # After build_ext is run, the following commands will run:
        # 
        # install_lib
        # install_scripts
        # 
        # These commands are subclassed above to avoid pitfalls that
        # setuptools tries to impose when installing these, as it usually
        # wants to build those libs and scripts as well or move them to a
        # different place. See comments above for additional information

setup(name='bpy',
      version="2.91",
      packages=find_packages(),
      ext_modules=[CMakeExtension(name="bpy")],
      entry_points={
          "console_scripts": [
              "bpy_post_install = "
              "blender.post_install:post_install",
              "bpy_pre_uninstall = "
              "blender.pre_uninstall:pre_uninstall"
          ]
      },
      description='Blender as a python module',
      long_description=open("./README.rst", 'r').read(), # <-- needs to be copied
      keywords="Blender, 3D, Animation, Renderer, Rendering",
      classifiers=["Development Status :: 3 - Alpha",
                   "Environment :: Win32 (MS Windows)",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: "
                   "GNU General Public License v3 (GPLv3)",
                   "Natural Language :: English",
                   "Operating System :: MacOS",
                   "Operating System :: POSIX :: Linux",
                   "Operating System :: Microsoft :: Windows",
                   "Programming Language :: C",
                   "Programming Language :: C++",
                   "Programming Language :: Python :: Implementation :: "
                   "CPython",
                   "Topic :: Artistic Software",
                   "Topic :: Education",
                   "Topic :: Multimedia",
                   "Topic :: Multimedia :: Graphics",
                   "Topic :: Multimedia :: Graphics :: 3D Modeling",
                   "Topic :: Multimedia :: Graphics :: 3D Rendering",
                   "Topic :: Games/Entertainment"],
      author='Blender Foundation',
      author_email='bf-committers@blender.org',
      license='GPL-3.0',
      install_requires=["numpy"], # Because of audio
      url="http://git.blender.org/gitweb/",
      cmdclass={
          'build_ext': BuildCMakeExt,
          'install_data': InstallCMakeLibsData,
          'install_lib': InstallCMakeLibs,
          'install_scripts': InstallBlenderScripts
          }
     )
