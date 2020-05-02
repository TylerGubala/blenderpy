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

BLENDER_SCRIPTS_DIR_PATTERN = r"\d\.\d\d"
BLENDER_SCRIPTS_DIR_REGEX = re.compile(BLENDER_SCRIPTS_DIR_PATTERN)

EXECUTABLE_DIR = pathlib.Path(sys.executable).parent

SYSTEM_NAME = platform.system()

def find_blender_scripts_directory(search_root: str) -> Optional[str]:

    for _dir, _dirs, _files in os.walk(search_root):

        if re.match(BLENDER_SCRIPTS_DIR_REGEX, os.path.basename(_dir)) and\
           all([entry in _dirs for entry in ["datafiles", "scripts"]]):

            return _dir

    return None

def move_to_executable_dir(path: pathlib.Path):

    destination = str(EXECUTABLE_DIR.absolute())

    if str(path.parent.absolute()).casefold() == destination.casefold():

        # Do not need to move path, it already exists alongside executable

        print(path+" already direct child of "+destination)

    else:

        print("Moving "+path+" to "+destination)

        shutil.move(str(path.absolute()), str(destination))

def move_to_macos_release_dir(path: pathlib.Path):

    destination = os.path.join(str(EXECUTABLE_DIR.parent.parent.absolute()), "lib", "Release")

    os.makedirs(destination, exist_ok=True)

    if str(path.parent.absolute()).casefold() == destination.casefold():

        # Do not need to move path, it already exists at MacOS specific location

        print(path+" already direct child of "+destination)

    else:

        print("Moving "+path+" to "+destination)

        shutil.move(str(path.absolute()), str(destination))

def install_scripts_directory():

    if SYSTEM_NAME == "Linux":

        print("No need to move scripts on Linux, skipping")

    elif SYSTEM_NAME == "Windows":

        blender_scripts_directory = None

        if os.path.basename(str(EXECUTABLE_DIR)).casefold() \
           == "scripts".casefold():

           # User is in venv (probably)

           blender_scripts_directory = find_blender_scripts_directory(str(EXECUTABLE_DIR.parent.parent.absolute()))

        else:

            # User is in system python (probably)

            blender_scripts_directory = find_blender_scripts_directory(str(EXECUTABLE_DIR.parent.absolute()))

        if blender_scripts_directory is None:

            raise Exception("Cannot find Blender scripts directory, "
                            "cannot continue")

        else:

            move_to_executable_dir(pathlib.Path(blender_scripts_directory))

    elif SYSTEM_NAME == "Darwin":

        blender_scripts_directory = find_blender_scripts_directory(str(EXECUTABLE_DIR.parent.parent.absolute()))

        if blender_scripts_directory is None:

            raise Exception("Cannot find Blender scripts directory, "
                            "cannot continue")

        else:

            move_to_macos_release_dir(pathlib.Path(blender_scripts_directory))

    else:

        print("Cannot determine system type, "
              "skipping move of scripts directory")

def post_install():

    install_scripts_directory()
