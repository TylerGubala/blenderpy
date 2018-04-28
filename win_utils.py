"""
windows build utilities convenience functions
"""

import ctypes
import os
import shutil
import site
import subprocess
import sys
from typing import Optional
import winreg

# site-packages dependencies imports
from git import Repo
import svn

# local imports
import common_utils

def is_admin():
    """
    Check if the user is a windows administrator

    Only works on windows at the moment due to a bug I experienced doing a
    Repo.submodule_update(), help wanted here to see what really went wrong;
    will try to reproduce the error
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin(program: Optional[str] = __file__):
    """
    If the user is not an adminstrator, elevate
    """

    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", 
                                            sys.executable, program, None, 1)

def get_vs_version():
    is_vs2013_available = False
    is_vs2015_available = False
    is_vs2017_available = False

    result = None

    # check for vs2013
    try:
        winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, 'VisualStudio.DTE.12.0')
    except:
        pass
    else:
        is_vs2013_available = True
        result = 2013

    # Check for vs2015
    try:
        winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, 'VisualStudio.DTE.14.0')
    except:
        pass
    else:
        is_vs2015_available = True
        result = 2015

    # Check for vs2017
    try:
        winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, 'VisualStudio.DTE.15.0')
    except:
        pass
    else:
        is_vs2017_available = True
        result = 2017

    if all([not available for available in [is_vs2013_available, 
                                            is_vs2015_available,
                                            is_vs2017_available]]):

        raise Exception("Visual Studio 13 (or higher) and c++ build tools are "
                        "required to build blender as a module, please "
                        "install Visual Studio and the c++ build tools too")

    return result

VS_VERSION =  get_vs_version()

VS_LIBS = "lib/win64_vc12" if VS_VERSION == 2013 else "lib/win64_vc14"

BLENDER_SVN_REPO_URL = (f"https://svn.blender.org/svnroot/bf-blender/trunk/"
                        f"{VS_LIBS}")

def get_blender_sources(root_dir: str):
    """
    Grab the sources from the git repo, as well as some windows libs from svn

    The windows libs from svn are specific to the windows build process,
    whereas linux just uses apt-get
    """
    # Root dir contains the blender directory as well as the lib and 
    # vs directory

    try:

        common_utils.get_blender_git_sources(root_dir)

    except Exception as e:

        print("The submodule update function may have failed due to "
              "insufficient permissions; try running again with "
              "elevated permissions.")

        if input("Would you like to try "
                 "running again as admin? (Y/N)").upper() in ["Y", "YES"]:

            run_as_admin(__file__)

        else:

            raise e

    # Get the code contained in the svn repo

    print(f"Getting svn code modules from {BLENDER_SVN_REPO_URL}")

    lib_dir = os.path.join(root_dir, VS_LIBS)

    blender_svn_repo = svn.remote.RemoteClient(BLENDER_SVN_REPO_URL)

    blender_svn_repo.checkout(lib_dir)

    print(f"Svn code modules checked out successfully into {lib_dir}")

def configure_blender_as_python_module(root_dir: str):
    """
    using a call to cmake, set the blender project to build as a python module

    DEPRECIATED: we can now simply call 'make bpy <version>'; do not use this
    function
    """

    print("Configuring Blender project as python module...")

    try:

        build_dir_name = ("build_windows_Release_x64_vc15_Release")

        build_dir = os.path.join(root_dir, build_dir_name)

        os.makedirs(build_dir)

        subprocess.call(["cmake", "-D", "CMAKE_BUILD_TYPE=RELEASE", "-D",
                         "WITH_PYTHON_INSTALL=OFF", "-D", "WITH_PLAYER=OFF", 
                         "-D", "WITH_PYTHON_MODULE=ON", build_dir])

    except Exception as e:

        print("Something went wrong... check the console output for now")

        raise e

    else:

        print("Blender successfully configured!")

def make_blender_python(root_dir: str) -> str:
    """
    Using the automated build script, make bpy with the correct C++ build utils
    """

    print("Making Blender from sources...")

    try:

        subprocess.call([os.path.join(root_dir, 'make.bat'), 'bpy', 
                         str(VS_VERSION)])

    except Exception as e:

        print("Make sure cmake is installed properly and that the prereqs "
              "described here are in place: https://wiki.blender.org/"
              "index.php/Dev:Doc/Building_Blender")

        raise e

    else:

        print("Built Blender python module successfully")

def install_blender_python(root_dir: str):
    """
    Copy files into the right places (what is the best way to do this?)

    version directory -> parent directory of current executable
    bpy.pyd -> site-packages/bpy of current environment
    *.dll besides python36.dll -> site-packages/bpy of current environment
    __init__.py (from this repo) -> site-packages/bpy of current environment
    """

    build_dir = None

    for dir_name in os.listdir(root_dir):

        if dir_name.startswith('build'): # This is the build directory

            build_dir = dir_name

            break

    if build_dir is None:

        raise Exception('Could not find the build dir')

    bin_dir = os.path.join(build_dir, 'bin/Release')

    init_to_copy = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                "__init__.py")

    bpy_to_copy = os.path.join(bin_dir, 'bpy.pyd')

    dirs_to_copy = [dir_name for dir_name in os.listdir(bin_dir) if
                    os.path.isdir(dir_name)]

    dlls_to_copy = [dll for dll in os.listdir(bin_dir) if
                   os.path.splitext(dll) == ".dll" and
                   not dll.startswith('python')]

    bpy_package_dir = os.path.join(site.getsitepackages(), 'bpy')

    print(f"Making a package for bpy at: {bpy_package_dir}")

    os.makedirs(bpy_package_dir)

    python_exe_dir = os.path.dirname(sys.executable)

    print("Copying files...")

    shutil.copy(init_to_copy, bpy_package_dir)

    shutil.copy(bpy_to_copy, bpy_package_dir)

    for dll in dlls_to_copy:

        shutil.copy(dll, bpy_package_dir)

    for dir_name in dirs_to_copy:

        common_utils.recursive_copy(dir_name, python_exe_dir)

def find_blender_python(root_dir: str) -> str:
    """
    Find the containing folder for bpy.pyd, all module contents are relative
    """

    for dir_name, dir_path, file_names in os.walk(root_dir):

        if 'bpy.pyd' in file_names:

            return dir_name

    raise Exception(f"Blender python module failed to build; "
                    f"we could not find it in {root_dir}")