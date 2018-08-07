# blenderpy
Blender as a python module with easy-install

Meant for installation into a virtualenv or wherever, for unit testing of Blender extensions being authored, or developement of a Blender 3d-enabled Python application.

## Option 1 - Get prebuilt bdist_wheel from pypi

### Prerequisites

1. A supported python installation with pip installed

### Installation

`py -m pip install bpy`

## Option 2 - Build from sources using pypi

### Prerequisites

1. Windows users must have Visual Studio 2013 or later and C++ build tools installed to build from sources
2. Windows users must have an SVN provider to build from sources (see )
3. All users must `py -m pip install cmake` in their python environment to build from sources (currently adding it as a `setup_requires` does not install it properly); after build it may be uninstalled with `py -m pip uninstall cmake`
4. Users of Python versions below 3.6 must have `future-fstrings` installed `pip install -U future-fstrings`
5. Users of Python versions 3.4 and below will probably need to update `setuptools` `pip install -U setuptools`
6. Up-to-date `wheel`

### Installation

`py -m pip install bpy --no-binary`

### How it works

0. Create overriding classes CMakeExtension & BuildCMake, which inheirit from the setuptools classes; bpy is a python extension (.pyd) and an instance of CMakeExtension, BuildCMake is the command that is run when installing the extension from pip (or running setup.py)
1. Using GitPython, clone Blender sources from https://git.blender.org/
2. If on Windows, detect the installed version of Visual Studio and 64bit vs 32bit, and download the appropriate svn library based on that
3. Using cmake, configure blender as a python module per the Ideasman42 wiki page (now defunct) https://wiki.blender.org/wiki//User:Ideasman42/BlenderAsPyModule; configure this build solution in the build_temp directory of the bpy package
4. Using cmake, build the configured solution
5. Place the built binaries in the built extension parent directory (important!)
6. Relocate the /<Version> directory (i.e: /2.79) into the directory containing the executable from which this installation was spawned (where 'python.exe' is)
7. Clean up using the remaining functionality from the superclasses `build_ext` and `Extension`
8. bpy.pyd/ .so should now be installed into the site-packages

### Gotchas

I have not tested this for platforms other than Windows at the moment. More to come soon.

## Support this project

<a href="https://www.patreon.com/bePatron?u=3979551" data-patreon-widget-type="become-patron-button"><img src="https://cloakandmeeple.files.wordpress.com/2017/06/become_a_patron_button3x.png?w=610" width="180px"></a>

[![Support via PayPal](https://cdn.rawgit.com/twolfson/paypal-github-button/1.0.0/dist/button.svg)](https://www.paypal.me/tylergubala/)