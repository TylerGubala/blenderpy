#! /usr/bin/python
# -*- coding: utf-8

import os
import pathlib
import platform
import re
import shutil
import sys
import typing
from typing import Optional

# Monkey-patch 3.4 and below

if sys.version_info < (3,5):

    def home_path() -> pathlib.Path:

        return pathlib.Path(os.path.expanduser("~"))

    pathlib.Path.home = home_path

BLENDER_SCRIPTS_DIR_PATTERN = r"\d\.\d\d"
BLENDER_SCRIPTS_DIR_REGEX = re.compile(BLENDER_SCRIPTS_DIR_PATTERN)

EXECUTABLE_DIR = pathlib.Path(sys.executable).parent

BLENDER_SCRIPTS_INSTALL_DIR_LINUX = os.path.join(str(EXECUTABLE_DIR.parent.absolute()), 
                                                 "lib", "python"+str(sys.version_info[0])+"."+str(sys.version_info[1]), 
                                                 "site-packages")
BLENDER_SCRIPTS_INSTALL_DIR_MACOS = os.path.join(str(EXECUTABLE_DIR.parent.absolute()), 
                                                 "lib", "python"+str(sys.version_info[0])+"."+str(sys.version_info[1]), 
                                                 "Resources")
BLENDER_SCRIPTS_INSTALL_DIR_WINDOWS = str(EXECUTABLE_DIR.absolute())

SYSTEM_NAME = platform.system()

class OSIsUnknownError(Exception):
    """Error for when we cannot determine the OS
    """
    pass

class BlenderScriptsDirUnknownError(Exception):
    """Error for when we can't find the Blender scripts dir
    """

    pass

def find_blender_scripts_directory(search_root: str) -> Optional[str]:

    for _dir, _dirs, _files in os.walk(search_root):

        if re.match(BLENDER_SCRIPTS_DIR_REGEX, os.path.basename(_dir)) and\
           all([entry in _dirs for entry in ["datafiles", "scripts"]]):

            return _dir

    return None

def install_scripts_directory():

    blender_scripts_search_root_dir = None
    blender_scripts_install_dir = None

    if SYSTEM_NAME == "Linux":

        blender_scripts_search_root_dir = str(EXECUTABLE_DIR.parent.parent.absolute())
        blender_scripts_install_dir = BLENDER_SCRIPTS_INSTALL_DIR_LINUX

    elif SYSTEM_NAME == "Windows":

        blender_scripts_install_dir = BLENDER_SCRIPTS_INSTALL_DIR_WINDOWS

        if os.path.basename(str(EXECUTABLE_DIR)).casefold() \
           == "scripts".casefold():

           # User is in venv (probably)

           blender_scripts_search_root_dir = str(EXECUTABLE_DIR.parent.parent.absolute())

        else:

            # User is in system python (probably)

            blender_scripts_search_root_dir = str(EXECUTABLE_DIR.parent.absolute())

    elif SYSTEM_NAME == "Darwin":

        blender_scripts_search_root_dir = str(EXECUTABLE_DIR.parent.parent.absolute())

        blender_scripts_install_dir = BLENDER_SCRIPTS_INSTALL_DIR_MACOS

    else:

        raise OSIsUnknownError("Cannot determine system type, "
                               "skipping move of scripts directory")

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
