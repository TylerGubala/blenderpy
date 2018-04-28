"""
MacOS builds convenience functions

Warning: this is basically extremely experimental
TODO: Better testing on MacOS side of things
"""

import os
import site
import subprocess
import sys

import cmake

from common_utils import get_blender_git_sources as get_blender_sources
from linux_utils import make_blender_python, find_blender_python

def install_blender_python(root_dir: str):
    """
    Copy 2.79 into site-packages, copy bpy.so into the site packages

    Directly copied information from 
    https://wiki.blender.org/index.php/User:Ideasman42/BlenderAsPyModule

    TODO: Check for correctness
    """

    bpy_path = os.path.join(root_dir, 'bin/bpy.so')
    ver_dir = os.path.join(root_dir, 'bin/2.79')

    subprocess.call(['cp', bpy_path, site.getsitepackages()])

    subprocess.call(['cp', '-R', ver_dir, site.getsitepackages()])
