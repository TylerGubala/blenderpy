#! /usr/bin/python
# -*- coding: utf-8 -*-
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
from wheel.bdist_wheel import bdist_wheel

# Monkey-patch 3.4 and below

if sys.version_info < (3,5):

    def home_path() -> pathlib.Path:

        return pathlib.Path(os.path.expanduser("~"))

    pathlib.Path.home = home_path

PYTHON_EXE_DIR = os.path.dirname(sys.executable)

SYSTEM_OS_NAME = platform.system()

# Change the Blender desired API version variable to build different versions
# of the Blender API. For instance, 'v2.79b' is the same version of the API
# as you would get when opening the Blender application at v2.79b
VERSION = "3.20"
VERSION_TUPLE = pkg_resources.parse_version(VERSION)

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

            # Copy the blender scripts directory

            shutil.copytree(scripts_dir,
                            os.path.join(self.build_dir,
                                     os.path.basename(scripts_dir)))

        # Mark the scripts for installation, adding them to 
        # distribution.scripts seems to ensure that the setuptools' record 
        # writer appends them to installed-files.txt in the package's egg-info

        self.distribution.scripts = scripts_dirs

        super().run()

class CMakeBuild(bdist_wheel):
    """Create custom build 
    """

    user_options = bdist_wheel.user_options + [
        ("bpy-prebuilt=", None, "Location of prebuilt bpy binaries"),
        ("bpy-cmake-configure-args=", None, "Custom CMake options")
    ]

    def initialize_options(self):
        """Allows for `cmake_extension_prebuild_dir`
        """

        super().initialize_options()
        self.bpy_prebuilt = None
        self.bpy_cmake_configure_args = None

class BuildCMakeExt(build_ext):
    """
    Builds using cmake instead of the python setuptools implicit build
    """
    user_options = build_ext.user_options + [
        ("bpy-prebuilt=", None, "Location of prebuilt bpy binaries"),
        ("bpy-cmake-configure-args=", None, "Custom CMake options")
    ]

    def initialize_options(self):
        """Allows for `cmake_extension_prebuild_dir`
        """

        super().initialize_options()
        self.bpy_prebuilt = None
        self.bpy_cmake_configure_args = None

    def finalize_options(self):
        """Grab options from previous call to `build`

        This is required to get the options passed into --build-options
        during bdist_wheel creation
        """

        super().finalize_options()

        self.set_undefined_options('bdist_wheel',
                                   ('bpy_prebuilt', 'bpy_prebuilt'),
                                   ('bpy_cmake_configure_args',
                                    'bpy_cmake_configure_args')
                                   )

    def run(self):
        """
        Perform build_cmake before doing the 'normal' stuff
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

                if self.bpy_prebuilt: # user assumes responsibility
                                     # for built files

                    self.announce(f"Using supplied prebuilt path "
                                  f"{self.bpy_prebuilt}", level=3)

                    self.copy_bpy(self.bpy_prebuilt, extension_path)

                else: # we assume responsibility for built files

                    git_checkout_path = pathlib.Path(os.path.join(self.build_temp, "blender"))
                    build_path = pathlib.Path(os.path.join(self.build_temp, "build"))

                    os.makedirs(str(git_checkout_path), exist_ok=True)
                    os.makedirs(str(build_path), exist_ok=True)

                    self.build_bpy(git_checkout_path, self.build_temp, build_path)

        super().run()

    def build_bpy(self, git_checkout_path: pathlib.Path, 
                  svn_checkout_path: pathlib.Path, build_path: pathlib.Path):
        """
        The steps required to build the extension
        """
        # Import bpybuild here because otherwise the script will 
        # fail before bpybuilt is retrieved

        import bpybuild.sources
        import bpybuild.make

        self.announce("Searching for compatible Blender online "
                      "(this will take a while)", level=3)

        compatible_bpy = bpybuild.sources.get_compatible_sources()

        if not VERSION_TUPLE in compatible_bpy:

            raise Exception(f"{VERSION} bpy is not compatible with "
                            f"{SYSTEM_OS_NAME} Python {sys.version} "
                            f"{bpybuild.BITNESS}bit")

        self.announce(f"Found compatible Blender version {VERSION}", level=3)

        git_repo = compatible_bpy[VERSION_TUPLE][0][0]
        svn_repo = compatible_bpy[VERSION_TUPLE][1][0]
        # When using compatible_sources you always get a git and svn repo object

        self.announce("Cloning Blender source from git "
                      "(this will take a while)", level=3)

        git_repo.checkout(git_checkout_path) # Clones into 'blender'

        self.announce("Cloning precompiled libs from svn "
                      "(this will take a while)", level=3)

        svn_repo.checkout(svn_checkout_path) # Checkout into 'lib' (automatic)

        self.announce("Configuring cmake project and building binaries "
                      "(this will take a while)", level=3)

        for command in bpybuild.make.get_make_commands(source_location= git_checkout_path,
                                                       build_location= build_path,
                                                       cmake_configure_args = self.cmake_configure_args):

            self.spawn(command)

        # Build finished, now copy the files into the copy directory
        # The copy directory is the parent directory of the extension (.pyd)

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
      version="2.93a0",
      packages=find_packages(),
      ext_modules=[CMakeExtension(name="bpy")],
      entry_points={
          "console_scripts": [
              "bpy_post_install = "
              "blenderpy.post_install:post_install",
              "bpy_pre_uninstall = "
              "blenderpy.pre_uninstall:pre_uninstall"
          ]
      },
      description='Blender as a python module',
      long_description=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"README.md"), 'r').read(),
      long_description_content_type="text/markdown",
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
      author='Tyler Gubala',
      author_email='gubalatyler@gmail.com',
      license='GPL-3.0',
      python_requires=">=3.7, <3.8",
      install_requires=["numpy==1.19.3"],
      url="https://github.com/TylerGubala/blenderpy",
      cmdclass={
          'bdist_wheel': CMakeBuild,
          'build_ext': BuildCMakeExt,
          'install_data': InstallCMakeLibsData,
          'install_lib': InstallCMakeLibs,
          'install_scripts': InstallBlenderScripts
          },
      setup_requires=[
          "bpy-build",
          "wheel"
      ]
     )
