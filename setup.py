"""
Build blender into a python module
"""

import os
import pathlib
from setuptools import setup, find_packages
from setuptools.command.install import install as install_command
import site
import sys
# Tempfile will be used to create a temporary directory to build Blender in
import tempfile

from common_utils import is_linux, is_mac, is_windows

if is_linux():
    # linux imports go here
    from linux_utils import install_blender_python, get_blender_sources, make_blender_python
elif is_windows():
    # windows imports go here
    from win_utils import install_blender_python, get_blender_sources, make_blender_python
elif is_mac():
    # Mac imports goes here
    from mac_utils import install_blender_python, get_blender_sources, make_blender_python
else:
    raise OSError(f"This module does not support {sys.platform}")


class CustomInstallHandler(install_command):
    """
    Custom install command handler for pip install

    Allows for custom install routine
    """

    def run(self):
        """
        Make a temporary folder containing blender sources, then build blender
        """

        pass # TODO: Create a blender_build package on pypi that setup_requires

if os.path.basename(os.path.realpath(sys.executable)).startswith('blender'):

    raise Exception("You are already in blender, you do not need to build bpy!")

# with tempfile.TemporaryDirectory() as root_dir: Put blender instead at the 
# home directory under .blenderpy

root_dir = os.path.join(pathlib.Path.home(), '.blenderpy')

if not os.path.isdir(root_dir):

    os.makedirs(root_dir)

    print(f"Created directory {root_dir}")

else:

    print(f"Found blenderpy directory at {root_dir}")

get_blender_sources(root_dir)

make_blender_python(root_dir)

print("Make process complete, installing...")

# TODO: Here, how to make an extension library that grabs the built 
# blender libs and pyd/so file? Right now install blender python does
# this manually

install_blender_python(root_dir)

setup(name='bpy',
      version='0.0.1',
      packages=find_packages(),
      description='Blender as a python module',
      long_description=open('README.md').read(),
      author='Tyler Gubala',
      author_email='gubalatyler@gmail.com',
      license='GPL-3.0',
      setup_requires=[
          'blenderpy_build',
          'python-apt;platform_system=="Linux"'
      ],                   
      cmd_class={
          'install': CustomInstallHandler
      }
)