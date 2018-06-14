"""
Build blender into a python module

Depends upon the bpybuild package
"""

import os
import pathlib
from setuptools import find_packages, setup, Extension
from setuptools.command.build_ext import build_ext
import sys
from typing import List

class CMakeExtension(Extension):
    """
    An extension to run the cmake build
    """

    def __init__(self, name, sources=[]):

        self.name = name
        self.sources = sources

        super().__init__(name = self.name, sources = [])

class BuildCMakeExt(build_ext):
    """
    Builds using cmake instead of the python setuptools implicit build
    """

    def build_extension(self, extension):
        """
        The steps required to build the extension
        """

        print(f"Reached the build entrypoint for {extension}")

        if not extension == "bpy":

            super().build_extension(extension)

            return

        print(f"Performing special bpy build steps!")

        import cmake
        import git
        if sys.platform == 'win32': import svn

def get_sources() -> List[str]:
    """
    Get the complete list of sources for blender
    """

    result = []

    for directory_name, subdirectory_names, file_names in os.walk('./blender'):

        for file_name in file_names:

            if os.path.splitext(file_name)[1] in ['.c', '.cpp']:

                result.append(os.path.abspath(file_name))

    return result

def get_include_dirs() -> List[str]:
    """
    Get the complete list of the include directories for blender
    """

    result = []

    for directory_name, subdirectory_names, file_names in os.walk('./blender'):

        for file_name in file_names:

            if os.path.splitext(file_name)[1] in ['.h', '.hpp']:

                result.append(os.path.abspath(directory_name))

    return result

setup(name='bpy',
      version='1.0.0',
      packages=find_packages(),
      ext_modules={'bpy': Extension(name="bpy", sources=get_sources(), 
                   include_dirs=get_include_dirs(), library_dirs=['./lib'])},
      description='Blender as a python module',
      author='Tyler Gubala',
      author_email='gubalatyler@gmail.com',
      license='GPL-3.0',
      setup_requires=[
          "GitPython", 'cmake', 'svn;platform_system=="Windows"',
          'python-apt;platform_system=="Linux"'
      ],
      url="https://github.com/TylerGubala/blenderpy"
)