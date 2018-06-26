"""
Build blender into a python module

Depends upon the bpybuild package
"""

import os
import pathlib
from setuptools import find_packages, setup, Extension
from setuptools.command.build_ext import build_ext
import struct
import sys
from typing import List

BLENDER_GIT_REPO_URL = 'git://git.blender.org/blender.git'

class CMakeExtension(Extension):
    """
    An extension to run the cmake build
    """

    def __init__(self, name, sources=[]):

        super().__init__(name = name, sources = sources)

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

        from git import Repo

        blenderpy_dir = os.path.join(pathlib.Path.home, ".blenderpy")
        blender_dir = os.path.join(blenderpy_dir, "blender")

        build_dir = pathlib.Path(self.build_temp)
        extension_dir = pathlib.Path(self.get_ext_fullpath(extension.name))

        os.makedirs(blender_dir, exist_ok=True)
        os.makedirs(build_dir, exist_ok=True)
        os.makedirs(extension_dir, exist_ok=True)

        try:

            blender_git_repo = Repo(blender_dir)

        except:

            Repo.clone_from(BLENDER_GIT_REPO_URL, blender_dir)
            blender_git_repo = Repo(blender_dir)

        finally:
                
            blender_git_repo.heads.master.checkout()
            blender_git_repo.remotes.origin.pull()

        blender_git_repo.git.submodule('update', '--init', '--recursive')

        for submodule in blender_git_repo.submodules:
                
            submodule_repo = submodule.module()
            submodule_repo.heads.master.checkout()
            submodule_repo.remotes.origin.pull()

        if sys.platform == "win32":
                
            import svn.remote
            import winreg

            vs_versions = []

            for version in [12, 14, 15]:

                try:

                    winreg.OpenKey(winreg.HKEY_CLASSES_ROOT,
                                   f"VisualStudio.DTE.{version}.0")

                except:

                    pass
                    
                else:

                    vs_versions.append(version)

            if not vs_versions:

                raise Exception("Windows users must have "
                                "Visual Studio installed")

            svn_url = (f"https://svn.blender.org/svnroot/bf-blender/trunk/lib/"
                       f"{'windows_vc12' if max(vs_versions) == 12 else 'win_vc14'}")

            svn_dir = os.path.join(blenderpy_dir, "lib",
                                   f"windows_vc{max(vs_versions)}")

            os.makedirs(svn_dir, exist_ok=True)

            blender_svn_repo = svn.remote.RemoteClient(svn_url)
            blender_svn_repo.checkout(svn_dir)

        self.spawn(['cmake', '-H'+blender_dir, '-B'+self.build_temp,
                    '-DWITH_PLAYER=OFF', '-DWITH_PYTHON_INSTALL=OFF',
                    '-DWITH_PYTHON_MODULE=ON'])
        self.spawn(["cmake", "--build", self.build_temp, "--target build",
                    "--config Release"])

setup(name='bpy',
      version='1.2.0a0',
      packages=find_packages(),
      ext_modules=[CMakeExtension(name="bpy")],
      description='Blender as a python module',
      author='Tyler Gubala',
      author_email='gubalatyler@gmail.com',
      license='GPL-3.0',
      setup_requires=["cmake", "GitPython", 'svn;platform_system=="Windows"'],
      url="https://github.com/TylerGubala/blenderpy")
