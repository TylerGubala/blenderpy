#! /usr/bin/python
# -*- coding: utf-8
"""Post install script
"""

import os
import pathlib
import shutil

# Relative imports
from blenderpy import BlenderScriptsDirUnknownError,\
                      find_blender_scripts_directory,\
                      get_blender_scripts_install_dir,\
                      get_python_scripts_directory

def install_scripts_directory():

    blender_scripts_search_root_dir = get_python_scripts_directory()
    blender_scripts_install_dir = get_blender_scripts_install_dir()

    blender_scripts_current_dir = find_blender_scripts_directory(blender_scripts_search_root_dir)

    if blender_scripts_current_dir is not None:

        print("Found Blender scripts directory at " + blender_scripts_current_dir)

        if str(pathlib.Path(blender_scripts_current_dir).parent.absolute()).casefold() == blender_scripts_install_dir.casefold():

            print(blender_scripts_current_dir+" already direct child of "+blender_scripts_install_dir)

        else:

            print("Moving "+blender_scripts_current_dir+" to "+blender_scripts_install_dir)

            shutil.move(blender_scripts_current_dir, 
                        os.path.join(blender_scripts_install_dir, 
                                     os.path.basename(blender_scripts_current_dir)))

    else:

        raise BlenderScriptsDirUnknownError("Could not find Blender scripts "
                                            "directory in "
                                            +blender_scripts_search_root_dir)

def post_install():

    install_scripts_directory()
    print("Configuration complete, enjoy using Blender as a Python module!")
