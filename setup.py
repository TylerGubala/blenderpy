"""
Build blender into a python module
"""

import os
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

        if os.path.basename(os.path.realpath(sys.executable)).startswith('blender'):

            raise Exception("You are already in blender, you do not need to build bpy!")

        with tempfile.TemporaryDirectory() as root_dir:

            print(f"Created temporary directory {root_dir}")

            get_blender_sources(root_dir)

            make_blender_python(root_dir)

            print("Make process complete, installing...")

            # TODO: Here, how to make an extension library that grabs the built 
            # blender libs and pyd/so file? Right now install blender python does
            # this manually

            install_blender_python(root_dir)

if __name__ == "__main__":

    setup(name='bpy',
          version='0.0.1',
          packages=find_packages(),
          description='Blender as a python module',
          long_description=open('README.md').read(),
          author='Tyler Gubala',
          author_email='gubalatyler@gmail.com',
          license='GPL-3.0',
          install_requires=open('requirements.txt').readlines() +
                                ['python-apt'] if is_linux() else [],
          cmd_class={
            'install': CustomInstallHandler
          }
         )