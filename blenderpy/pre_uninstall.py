#! /usr/bin/python
# -*- coding: utf-8
"""Pre uninstall script
"""
import shutil

from blenderpy import BlenderScriptsDirUnknownError,\
                      find_blender_scripts_directory,\
                      get_blender_scripts_install_dir,\
                      get_python_scripts_directory

def remove_blender_scripts_dir():
    """Find and remove the blender scripts directory
    """

    blender_scripts_search_root_dir = get_blender_scripts_install_dir()

    blender_scripts_current_dir = find_blender_scripts_directory(blender_scripts_search_root_dir)

    if blender_scripts_current_dir is not None:

        print("Found blender scripts dir at "+blender_scripts_current_dir)
        print("Removing "+blender_scripts_current_dir)

        shutil.rmtree(blender_scripts_current_dir)

    else:

        print("Did not find Blender scripts at post_install script location")
        print("Did you forget to perform bpy_post_install after installing?")
        print("Searching original pip install location")

        blender_scripts_search_root_dir = get_python_scripts_directory()

        blender_scripts_current_dir = find_blender_scripts_directory(blender_scripts_search_root_dir)

        if blender_scripts_current_dir is not None:

            print("Found blender scripts dir at "+blender_scripts_current_dir)
            print("Removing "+blender_scripts_current_dir)

            shutil.rmtree(blender_scripts_current_dir)

        else:

            raise BlenderScriptsDirUnknownError("Could not find Blender scripts "
                                                "directory in "
                                                +blender_scripts_search_root_dir)

def pre_uninstall():
    print("Searching for and removing non-tracked files & folders")
    remove_blender_scripts_dir()
    print("Pre uninstall is complete")