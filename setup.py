"""
Build blender into a python module
"""

from distutils.command.build_clib import build_clib
import os
import pathlib
from setuptools import find_packages, setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.install_lib import install_lib
from setuptools.command.install_scripts import install_scripts
import shutil
import struct
import sys
from typing import List

PYTHON_EXE_DIR = os.path.dirname(sys.executable)

BLENDER_GIT_REPO_URL = 'git://git.blender.org/blender.git'
BLENDERPY_DIR = os.path.join(pathlib.Path.home(), ".blenderpy")

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

        self.distribution.libraries = [(os.path.basename(lib), {'sources': []})
                                       for lib in libs]

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

        self.announce(f"{os.path.abspath(bin_dir)}", level=3)

        for item in os.listdir(bin_dir):

            self.announce(f"{item}\t{'Directory' if os.path.isdir(os.path.join(bin_dir, item)) else 'File'}", level=3)

        scripts_dirs = [os.path.join(bin_dir, _dir) for _dir in
                        os.listdir(bin_dir) if
                        os.path.isdir(os.path.join(bin_dir, _dir))]

        for scripts_dir in scripts_dirs:

            shutil.move(scripts_dir, os.path.join(self.build_dir,
                                                  os.path.basename(scripts_dir)))

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

        from git import Repo

        self.announce("Preparing the build environment", level=3)

        blender_dir = os.path.join(BLENDERPY_DIR, "blender")

        build_dir = pathlib.Path(self.build_temp)

        # It may seem redundant, as we never actually use extension_dir
        # but creating extension_dir prevents the superclass from __also__
        # running `build_ext` on the bpy extension, so we must ensure that
        # this step takes place

        extension_path = pathlib.Path(self.get_ext_fullpath(extension.name))

        os.makedirs(blender_dir, exist_ok=True)
        os.makedirs(build_dir, exist_ok=True)
        os.makedirs(extension_path.parent.absolute(), exist_ok=True)

        self.announce(f"Cloning Blender source from {BLENDER_GIT_REPO_URL}", level=3)

        try:

            blender_git_repo = Repo(blender_dir)

        except:

            Repo.clone_from(BLENDER_GIT_REPO_URL, blender_dir)
            blender_git_repo = Repo(blender_dir)

        finally:
                
            blender_git_repo.heads.master.checkout()
            blender_git_repo.remotes.origin.pull()

        self.announce(f"Updating Blender git submodules", level=3)

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
            svn_dir = os.path.join(BLENDERPY_DIR, "lib", svn_lib)

            os.makedirs(svn_dir, exist_ok=True)

            self.announce(f"Checking out svn libs from {svn_url}", level=3)

            try:

                blender_svn_repo = svn.remote.RemoteClient(svn_url)
                blender_svn_repo.checkout(svn_dir)

            except Exception as e:

                self.warn("Windows users must have the svn executable "
                          "available from the command line")
                self.warn("Please install Tortoise SVN with \"command line "
                          "client tools\" as described here")
                self.warn("https://stackoverflow.com/questions/1625406/using-"
                          "tortoisesvn-via-the-command-line")
                raise e

        self.announce("Configuring cmake project", level=3)

        self.spawn(['cmake', '-H'+blender_dir, '-B'+self.build_temp,
                    '-DWITH_PLAYER=OFF', '-DWITH_PYTHON_INSTALL=OFF',
                    '-DWITH_PYTHON_MODULE=ON',
                    f"-DCMAKE_GENERATOR_PLATFORM=x"
                    f"{'86' if BITS == 32 else '64'}"])
        
        self.announce("Building binaries", level=3)

        self.spawn(["cmake", "--build", self.build_temp, "--target", "INSTALL",
                    "--config", "Release"])

        # Build finished, now copy the files into the copy directory
        # The copy directory must be one level up from the extension directory
        # This is to ensure the package imports successfully
        # If copied into the extension_dir, you will get .dll load failed
        # access denied errors

        self.announce("Moving Blender python module", level=3)

        bin_dir = os.path.join(build_dir, 'bin', 'Release')
        self.distribution.bin_dir = bin_dir

        bpy_path = [os.path.join(bin_dir, _bpy) for _bpy in
                    os.listdir(bin_dir) if
                    os.path.isfile(os.path.join(bin_dir, _bpy)) and
                    os.path.splitext(_bpy)[0].startswith('bpy') and
                    os.path.splitext(_bpy)[1] in [".pyd", ".so"]][0]

        shutil.move(bpy_path, extension_path)

        self.distribution.run_command('install_lib')
        self.distribution.run_command('install_scripts')

class BuildCMakeLibs(build_clib):
    """
    A command that suppresses the distutils.command.build_clib class

    Really, that's all it does. It is only there to catch the case where
    install_lib attempts to build a library from scratch using a compiler.
    """

    # This had to be made because otherwise setup.py kept complaining about
    # how the second element in the of each tuple in 'libraries' must be a
    # dictionary (build info)
    # 
    # it was expecting a set of macros to be defined I guess...? Help please

    def run(self):
        """
        Do absolutely nothing

        Waste everyone's time with a pointless docstring
        """

        # If anyone knows a better way to avoid the error above while I'd love
        # to hear it

        pass

    build_libraries = run

setup(name='bpy',
      version='1.2.2a14',
      packages=find_packages(),
      ext_modules=[CMakeExtension(name="bpy")],
      description='Blender as a python module',
      author='Tyler Gubala',
      author_email='gubalatyler@gmail.com',
      license='GPL-3.0',
      setup_requires=["cmake", "GitPython", 'svn;platform_system=="Windows"'],
      url="https://github.com/TylerGubala/blenderpy",
      cmdclass={
          'build_clib': BuildCMakeLibs,
          'build_ext': BuildCMakeExt,
          'install_lib': InstallCMakeLibs,
          'install_scripts': InstallBlenderScripts
          }
    )
