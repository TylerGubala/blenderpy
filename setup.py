"""
Build blender into a python module

Depends upon the bpybuild package
"""

from setuptools import find_packages, setup
from setuptools.command.install import install as install_command

class CustomInstallHandler(install_command):
    """
    Custom install command handler for pip install

    Allows for custom install routine
    """

    def run(self):
        """
        Make a temporary folder containing blender sources, then build blender
        """
        import bpybuild

        bpybuild.create_python_module()

setup(name='bpy',
      version='1.0.0',
      packages=find_packages(),
      description='Blender as a python module',
      author='Tyler Gubala',
      author_email='gubalatyler@gmail.com',
      license='GPL-3.0',
      setup_requires=[
          'bpybuild@1.0.0a0'
      ],                   
      cmdclass={
          'install': CustomInstallHandler
      },
      url="https://github.com/TylerGubala/blenderpy"
)