"""
Cross platform utilities for building blender
"""

import os
import shutil
import sys

from git import Repo

BLENDER_GIT_REPO_URL = 'git://git.blender.org/blender.git'

def is_linux():
    return sys.platform in ['linux', 'linux2']

def is_windows():
    return sys.platform == 'win32'

def is_mac():
    return sys.platform == 'darwin'

def get_blender_git_sources(root_dir: str):
    """
    Check out the most up to date blender sources

    TODO: Display progress somehow
    """

    repo_directory = os.path.join(root_dir, 'blender')

    os.makedirs(repo_directory)

    print(f"Cloning blender from {BLENDER_GIT_REPO_URL}")

    Repo.clone_from(BLENDER_GIT_REPO_URL, repo_directory)

    print(f"Blender successfully cloned into {repo_directory}")

    blender_git_repo = Repo(repo_directory)

    print("Updating submodules...")

    # The submodule update method may fail due to a permissions error

    # GitPython's implimentation of submodule_update (derived from the 
    # RootModule object's update command) automatically is recursive 
    # and autoinits, so we don't have to worry about that
    blender_git_repo.submodule_update()

    print(f"Submodules updated!")

    print("Checking out master for submodules")

    for submodule in blender_git_repo.submodules:

        submodule_repo = Repo(submodule)

        submodule_repo.heads.master.checkout()

        submodule_repo.remotes.origin.pull()

def recursive_copy(src: str, dst: str):

    os.chdir(src)
    for item in os.listdir():

        if os.path.isfile(item):
            shutil.copy(item, dst)

        elif os.path.isdir(item):
            new_dst = os.path.join(dst, item)
            os.mkdir(new_dst)
            recursive_copy(os.path.abspath(item), new_dst)