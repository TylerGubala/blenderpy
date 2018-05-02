"""
Linux blender build convenience functions

Currently this basically only works for ubuntu...
TODO: Work on other flavors of linux
"""

import os
import subprocess

import cmake

import common_utils

# Import apt cannot happen on non linux os, but mac may be able to share some
# common functions with linux for the purposes of building, so we need to 
# check for it so when mac imports, it does not fail
if common_utils.is_linux():
    import apt

BLENDER_BUILD_DEPENDENCIES = ['git', 'build-essential', 'cmake',
                              'cmake-curses-gui']

BLENDER_ADDTL_DEPENDENCIES = [
 'libfreetype6-dev',
 'libglew-dev',
 'libglu1-mesa-dev',
 'libjpeg-dev',
 'libpng12-dev',
 'libsndfile1-dev',
 'libx11-dev',
 'libxi-dev',
  # How to find current python version best guess and install the right one?
 'python3.5-dev',
  # TODO: Update the above for a more maintainable way of getting correct version
 'libalut-dev',
 'libavcodec-dev',
 'libavdevice-dev',
 'libavformat-dev',
 'libavutil-dev',
 'libfftw3-dev',
 'libjack-dev',
 'libmp3lame-dev',
 'libopenal-dev',
 'libopenexr-dev',
 'libopenjpeg-dev',
 'libsdl1.2-dev',
 'libswscale-dev',
 'libtheora-dev',
 'libtiff5-dev',
 'libvorbis-dev',
 'libx264-dev',
 'libspnav-dev']

def get_blender_sources(root_dir: str):
    """
    Install build requirements, dependencies, etc for linux
    """

    print("Performing installation of linux build dependencies...")

    apt_cache = apt.cache.Cache()

    apt_cache.update()

    # We need to re-open the apt-cache after performing the update to use the
    # Updated cache, otherwise we will still be using the old cache see: 
    # https://stackoverflow.com/questions/17537390/how-to-install-a-package-using-the-python-apt-api
    apt_cache.open()

    for build_requirement in BLENDER_BUILD_DEPENDENCIES:

        required_package = apt_cache[build_requirement]

        if required_package.is_installed:

            print(f"Build requirement {build_requirement} already satisfied")

        else:

            required_package.mark_install()

            # Committing the changes to the cache could fail due to privilages
            # Maybe we could try-catch this exception to elevate the privilages
            apt_cache.commit()

            print(f"Build requirement {build_requirement} installed")

    common_utils.get_blender_git_sources(root_dir)

    print("Trying automated installation of blender dependencies...")

    try:

        automated_deps_install_script = os.path.join(root_dir, 
                                                     'blender/build_files/'
                                                     'build_environment/'
                                                     'install_deps.sh')

        subprocess.call([automated_deps_install_script])

    except:

        print("Automated installation failed, trying manual installation of "
              "blender dependencies...")

        for addtl_requirement in BLENDER_ADDTL_DEPENDENCIES:

            required_package = apt_cache[addtl_requirement]

            if required_package.is_installed:

                print(f"Additional requirement {addtl_requirement} "
                      f"already satisfied")

            else:

                required_package.mark_install()

                # Committing the changes to the cache could fail due to privilages
                # Maybe we could try-catch this exception to elevate the privilages
                apt_cache.commit()

                print(f"Additional requirement {addtl_requirement} installed")

        print("Blender additional dependencies installed manually")

    else:
        
        print("Blender additional dependencies installed automatically")

def make_blender_python(root_dir: str):
    """
    Build the bpy module using the automatic configuration
    """

    make_script = os.path.join(root_dir, 'blender/make')

    subprocess.call([make_script, 'bpy'])

def install_blender_python(root_dir: str):
    """
    Install blender from the make script
    """

    make_script = os.path.join(root_dir, 'blender/make')

    subprocess.call([make_script, 'install'])

def find_blender_python(root_dir: str) -> str:
    """
    Find the containing folder for bpy.so, all module contents are relative
    """

    for dir_path, dir_names, file_names in os.walk(root_dir):

        if 'bpy.so' in file_names:
            
            return dir_path

    raise Exception(f"Blender python module failed to build; "
                    f"we could not find it in {root_dir}")
