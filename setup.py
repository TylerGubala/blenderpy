"""
Build blender into a python module

Depends upon the bpybuild package
"""

import os
import pathlib
from setuptools import find_packages, setup, Extension
from setuptools.command.build_ext import build_ext
import shutil
import struct
import sys
from typing import List

PYTHON_EXE_DIR = os.path.dirname(sys.executable)

BLENDER_GIT_REPO_URL = 'git://git.blender.org/blender.git'

BITS = struct.calcsize("P") * 8

def recursive_copy(src: str, dst: str):

    for shortname in os.listdir(src):

        fullname = os.path.join(src, shortname)

        if os.path.isfile(fullname):
            shutil.copy(fullname, dst)

        elif os.path.isdir(fullname):
            new_dst = os.path.join(dst, shortname)
            os.mkdir(new_dst)
            recursive_copy(os.path.abspath(fullname), new_dst)

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

        self.announce("Preparing the build environment", level=3)

        blenderpy_dir = os.path.join(pathlib.Path.home(), ".blenderpy")
        blender_dir = os.path.join(blenderpy_dir, "blender")

        build_dir = pathlib.Path(self.build_temp)

        # It may seem redundant, as we never actually use extension_dir
        # but creating extension_dir prevents the superclass from __also__
        # running `build_ext` on the bpy extension, so we must ensure that
        # this step takes place

        extension_dir = pathlib.Path(self.get_ext_fullpath(extension.name))

        os.makedirs(blender_dir, exist_ok=True)
        os.makedirs(build_dir, exist_ok=True)
        os.makedirs(extension_dir, exist_ok=True)

        self.announce(f"Cloning Blender source from {BLENDER_GIT_REPO_URL}...",
                      level=3)

        try:

            blender_git_repo = Repo(blender_dir)

        except:

            Repo.clone_from(BLENDER_GIT_REPO_URL, blender_dir)
            blender_git_repo = Repo(blender_dir)

        finally:
                
            blender_git_repo.heads.master.checkout()
            blender_git_repo.remotes.origin.pull()

        self.announce(f"Updating Blender git submodules...", level=3)

        blender_git_repo.git.submodule('update', '--init', '--recursive')

        for submodule in blender_git_repo.submodules:
                
            submodule_repo = submodule.module()
            submodule_repo.heads.master.checkout()
            submodule_repo.remotes.origin.pull()

        if sys.platform == "win32": # Windows only steps
                
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

            svn_lib = (f"win{'dows' if BITS == 32 else '64'}"
                       f"{'_vc12' if max(vs_versions) == 12 else '_vc14'}")
            svn_url = (f"https://svn.blender.org/svnroot/bf-blender/trunk/lib/"
                       f"{svn_lib}")
            svn_dir = os.path.join(blenderpy_dir, "lib", svn_lib)

            os.makedirs(svn_dir, exist_ok=True)

            self.announce(f"Checking out svn libs from {svn_url}...", level=3)

            blender_svn_repo = svn.remote.RemoteClient(svn_url)
            blender_svn_repo.checkout(svn_dir)

        self.announce("Configuring cmake project...", level=3)

        self.spawn(['cmake', '-H'+blender_dir, '-B'+self.build_temp,
                    '-DWITH_PLAYER=OFF', '-DWITH_PYTHON_INSTALL=OFF',
                    '-DWITH_PYTHON_MODULE=ON',
                    f"-DCMAKE_GENERATOR_PLATFORM=x"
                    f"{'86' if BITS == 32 else '64'}"])
        
        self.announce("Building binaries...", level=3)

        self.spawn(["cmake", "--build", self.build_temp, "--target", "INSTALL",
                    "--config", "Release"])

        # Build finished, now copy the files into the copy directory
        # The copy directory must be one level up from the extension directory
        # This is to ensure the package imports successfully
        # If copied into the extension_dir, you will get .dll load failed
        # access denied errors

        self.announce("Copying files and cleaning up...", level=3)

        copy_dir = extension_dir.parent.absolute()

        bin_dir = os.path.join(build_dir, 'bin', 'Release')

        bins_to_copy = [os.path.join(bin_dir, _bin) for _bin in 
                        os.listdir(bin_dir) if 
                        os.path.isfile(os.path.join(bin_dir, _bin)) and 
                        os.path.splitext(_bin)[1] in [".pyd", ".dll", ".so"]
                        and not _bin.startswith("python")]

        for _bin in bins_to_copy:

            shutil.copy(_bin, copy_dir)
        
        dirs_to_copy = [os.path.join(bin_dir, folder) for folder in 
                        os.listdir(bin_dir) if 
                        os.path.isdir(os.path.join(bin_dir, folder))]
        
        for dir_name in dirs_to_copy:

            dir_basename = os.path.basename(dir_name)
            dir_newname = os.path.join(PYTHON_EXE_DIR, dir_basename)

            try:
        
                os.makedirs(dir_newname, exist_ok=True)

            except FileExistsError:

                pass

            else:

                pass

            recursive_copy(dir_name, dir_newname)

setup(name='bpy',
      version='1.2.1',
      packages=find_packages(),
      ext_modules=[CMakeExtension(name="bpy")],
      description='Blender as a python module',
      author='Tyler Gubala',
      author_email='gubalatyler@gmail.com',
      license='GPL-3.0',
      setup_requires=["cmake", "GitPython", 'svn;platform_system=="Windows"'],
      url="https://github.com/TylerGubala/blenderpy",
      cmdclass={'build_ext': BuildCMakeExt})
