#! /usr/bin/python
# -*- coding: utf-8
"""Installation / uninstallation helper scripts
"""

import os
import pathlib
import platform
import re
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

PYTHON_SCRIPTS_DIR_WINDOWS_SYSPYTHON = str(EXECUTABLE_DIR.parent.absolute())
PYTHON_SCRIPTS_DIR_WINDOWS_VENPYTHON = str(EXECUTABLE_DIR.parent.parent.absolute())
PYTHON_SCRIPTS_DIR_UNIX = str(EXECUTABLE_DIR.parent.parent.absolute())

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

def get_python_scripts_directory() -> str:
    if SYSTEM_NAME in ["Darwin", "Linux"]:

        return PYTHON_SCRIPTS_DIR_UNIX

    elif SYSTEM_NAME == "Windows":

        if os.path.basename(str(EXECUTABLE_DIR)).casefold() \
           == "scripts".casefold():

           # User is in venv (probably)

           return PYTHON_SCRIPTS_DIR_WINDOWS_VENPYTHON

        else:

            # User is in system python (probably)

            return PYTHON_SCRIPTS_DIR_WINDOWS_SYSPYTHON

    else:

        raise OSIsUnknownError("Cannot determine system type: "+SYSTEM_NAME)

def get_blender_scripts_install_dir() -> str:
    if SYSTEM_NAME == "Darwin":

        return BLENDER_SCRIPTS_INSTALL_DIR_MACOS

    elif SYSTEM_NAME == "Linux":

        return BLENDER_SCRIPTS_INSTALL_DIR_LINUX

    elif SYSTEM_NAME == "Windows":

        return BLENDER_SCRIPTS_INSTALL_DIR_WINDOWS

    else:

        raise OSIsUnknownError("Cannot determine system type: "+SYSTEM_NAME)