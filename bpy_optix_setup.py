#! /usr/bin/python
# -*- coding: future_fstrings -*-
"""
Build blender into a python module
"""

from distutils.command.install_data import install_data
import os
import pathlib
import pkg_resources
import platform
import re
from setuptools import find_packages, setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install
from setuptools.command.install_lib import install_lib
from setuptools.command.install_scripts import install_scripts
import shutil
import struct
import sys
from typing import List, Set

# Monkey-patch 3.4 and below

if sys.version_info < (3,5):

    def home_path() -> pathlib.Path:

        return pathlib.Path(os.path.expanduser("~"))

    pathlib.Path.home = home_path

PYTHON_EXE_DIR = os.path.dirname(sys.executable)

# Change the Blender desired API version variable to build different versions
# of the Blender API. For instance, 'v2.79b' is the same version of the API
# as you would get when opening the Blender application at v2.79b
VERSION = "2.81"
VERSION_TUPLE = pkg_resources.parse_version(VERSION)

# Optix render is only supported with versions greater than 2.81!
MIN_VERSION = "2.81"
MIN_VERSION_TUPLE = pkg_resources.parse_version(MIN_VERSION)

if VERSION < MIN_VERSION:

    raise ValueError(f"Blender version must be higher than {MIN_VERSION} (got {VERSION})")

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

        # There seems to be no other way to do this; I tried listing the
        # libraries during the execution of the InstallCMakeLibs.run() but
        # setuptools never tracked them, seems like setuptools wants to
        # track the libraries through package data more than anything...
        # help would be appriciated

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
        #
        # Also tried adding the libraries to the distribution.libraries list, 
        # but that never seemed to add them to the installed-files.txt in the 
        # egg-info, and the online recommendation seems to be adding libraries 
        # into eager_resources in the call to setup(), which I think puts them 
        # in data_files anyways. 
        # 
        # What is the best way?

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

            shutil.move(scripts_dir,
                        os.path.join(self.build_dir,
                                     os.path.basename(scripts_dir)))

        # Mark the scripts for installation, adding them to 
        # distribution.scripts seems to ensure that the setuptools' record 
        # writer appends them to installed-files.txt in the package's egg-info

        self.distribution.scripts = scripts_dirs

        super().run()

class BuildCMakeExt(build_ext):
    """
    Builds using cmake instead of the python setuptools implicit build
    """

    def run(self):
        """
        Perform build_cmake before doing the 'normal' stuff
        """

        for extension in self.extensions:

            if extension.name == "bpy":

                self.build_cmake(extension)

        super().run()

    def build_cmake(self, extension: Extension):
        """
        The steps required to build the extension
        """
        # Import bpy-make here because otherwise the script will 
        # fail before bpy-make is retrieved

        import bpymake.sources
        import bpymake.make

        self.announce("Preparing the build environment", level=3)

        setup_root_path = pathlib.Path(self.build_temp)
        blender_path = pathlib.Path(os.path.join(self.build_temp, "blender"))
        # lib_path = pathlib.Path(os.path.join(self.build_temp, "lib"))
        build_path = pathlib.Path(os.path.join(self.build_temp, "build"))
        extension_path = pathlib.Path(self.get_ext_fullpath(extension.name))

        os.makedirs(str(blender_path), exist_ok=True)
        os.makedirs(str(build_path), exist_ok=True)
        # os.makedirs(str(lib_path), exist_ok=True)
        os.makedirs(str(extension_path.parent.absolute()), exist_ok=True)

        self.announce("Searching for compatible Blender online "
                      "(this will take a while)", level=3)

        compatible_bpy = bpymake.sources.get_compatible_sources()

        if not VERSION_TUPLE in compatible_bpy:

            raise Exception(f"{VERSION} bpy is not compatible with "
                            f"{platform.system()} Python {sys.version} "
                            f"{bpymake.BITNESS}bit")

        self.announce(f"Found compatible Blender version {VERSION}", level=3)

        git_repo = compatible_bpy[VERSION_TUPLE][0][0]
        svn_repo = compatible_bpy[VERSION_TUPLE][1][0]
        # When using compatible_sources you always get a git and svn repo object

        self.announce(f"Cloning Blender source from git", level=3)

        git_repo.checkout(blender_path) # Clones into 'blender'

        self.announce(f"Cloning precompiled libs from svn", level=3)

        svn_repo.checkout(setup_root_path) # Checkout into 'lib' (automatic)

        self.announce(" Configuring cmake project "
                      "and building binaries", level=3)

        configure_commands = bpymake.make.get_make_commands(source_location= blender_path,
                                                            build_location= build_path)
                      
        optix_root = None

        if platform.system() == "Windows":

            optix_root = r"C:\ProgramData\NVIDIA Corporation\OptiX SDK 7.0.0"

        else:

            pass # TODO: Need help with other platforms

        if optix_root is None:

            raise Exception("Could not guess where Optix SDK is.")

        configure_commands[-1] += ["-DWITH_CYCLES_DEVICE_OPTIX=ON",
                                   f"-DOPTIX_ROOT_DIR={optix_root}"]

        for command in configure_commands:

            self.spawn(command)

        # Build finished, now copy the files into the copy directory
        # The copy directory is the parent directory of the extension (.pyd)

        self.announce("Moving Blender python module", level=3)

        bin_dir = None

        if platform.system() == "Windows":

            bin_dir = os.path.join(str(build_path), 'bin', 'Release')

        else:

            bin_dir = os.path.join(str(build_path), 'bin')
            
        self.distribution.bin_dir = bin_dir

        bpy_path = [os.path.join(bin_dir, _bpy) for _bpy in
                    os.listdir(bin_dir) if
                    os.path.isfile(os.path.join(bin_dir, _bpy)) and
                    os.path.splitext(_bpy)[0].startswith('bpy') and
                    os.path.splitext(_bpy)[1] in [".pyd", ".so"]][0]

        shutil.move(str(bpy_path), str(extension_path))

        # After build_ext is run, the following commands will run:
        # 
        # install_lib
        # install_scripts
        # 
        # These commands are subclassed above to avoid pitfalls that
        # setuptools tries to impose when installing these, as it usually
        # wants to build those libs and scripts as well or move them to a
        # different place. See comments above for additional information

setup(name='bpy-optix',
      version=VERSION,
      packages=find_packages(),
      ext_modules=[CMakeExtension(name="bpy")],
      entry_points={
          "console_scripts": [
              "bpy_post_install = "
              "blenderpy.post_install.post_install"
          ]
      },
      description='Blender as a python module',
      long_description=open("./README.md", 'r').read(),
      long_description_content_type="text/markdown",
      keywords="Blender, 3D, Animation, Renderer, Rendering",
      classifiers=["Development Status :: 3 - Alpha",
                   "Environment :: Win32 (MS Windows)",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: "
                   "GNU General Public License v3 (GPLv3)",
                   "Natural Language :: English",
                   "Operating System :: Microsoft :: Windows :: Windows 10",
                   "Programming Language :: C",
                   "Programming Language :: C++",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 3.4",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.7",
                   "Programming Language :: Python :: Implementation :: "
                   "CPython",
                   "Topic :: Artistic Software",
                   "Topic :: Education",
                   "Topic :: Multimedia",
                   "Topic :: Multimedia :: Graphics",
                   "Topic :: Multimedia :: Graphics :: 3D Modeling",
                   "Topic :: Multimedia :: Graphics :: 3D Rendering",
                   "Topic :: Games/Entertainment"],
      author='Tyler Gubala',
      author_email='gubalatyler@gmail.com',
      license='GPL-3.0',
      python_requires=">=3.4.0",
      setup_requires=["bpy-make", "future-fstrings"],
      url="https://github.com/TylerGubala/blenderpy",
      cmdclass={
          'build_ext': BuildCMakeExt,
          'install_data': InstallCMakeLibsData,
          'install_lib': InstallCMakeLibs,
          'install_scripts': InstallBlenderScripts
          }
     )
