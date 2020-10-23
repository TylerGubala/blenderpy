# blenderpy
Blender as a python module with easy-install

## About

Meant for installation into a virtualenv or wherever, for unit testing of Blender extensions being authored, or developement of a Blender 3d-enabled Python application.

Depends upon the `bpy-build` module to make sure the Blender `bpy` module environment is correct.

For more information, please see:

[bpy-build repository](https://github.com/TylerGubala/bpy-build)

## Getting Started

Prebuilt wheels are provided for popular Platforms (MacOS, Windows, and `manylinux`). Prebuilds are complete builds with audio, CUDA, and Optix functionality, like you would expect with installing the complete application.

## Prerequisites

Both building the Python package from sources and installing the `wheel` files require [the bare minimum dependencies listed on the Blender 3D wiki for building Blender](https://wiki.blender.org/wiki/Building_Blender). **Get these first before opening a new issue**.

### Installing

Installing from `pypi`:

`pip install bpy && bpy_post_install`

Installing from `wheel` file (see [Releases](https://github.com/TylerGubala/blenderpy/releases) page):

`pip install <PATH_TO_WHEEL_FILE> && bpy_post_install`

### Uninstalling

A unique uninstallation script is required to ensure that all traces of `bpy` are removed from the hard drive, because Blender expects `.dll` and `.so` libraries to be in places that are not part of the Python packaging system.

`bpy_pre_uninstall && pip uninstall bpy`

### Building

See more about building `bpy` [on the wiki page](https://github.com/TylerGubala/blenderpy/wiki/Building).

## FAQ

### Q. I am getting `failed to find 'bpy_types' module`

A. Please see [issue #13](https://github.com/TylerGubala/blenderpy/issues/13)

### Q. I am getting `ImportError: DLL load failed: The specified module could not be found`

A. Please see [issue #15](https://github.com/TylerGubala/blenderpy/issues/15)

### Q. How do I import addons?

A. Addons (Blender internal and third party) can be imported using the code [referenced here](https://github.com/TylerGubala/blenderpy/wiki/Caveat---Importing-Addons).

### Q. How can I use Blender in `multiprocessing`?

A. Blender runtime usage and compatibility with `multiprocessing` is limited, see [the documentation](https://github.com/TylerGubala/blenderpy/wiki/Caveat---Usage-with-multiprocessing).

### Q. What about my operating system of choice?

A. Please file a new issue if you are having trouble installing on your operating system of choice.

### Q. What about my Python version of choice?

A. Some builds you will have to make yourself if you have a specific version of the API you want. Likewise, if you are contrained to a specific Python version (especially those that aren't shipped by python.org) then you may have to try and build yourself.

### Q. What about my bitness of choice?

A. 32-bit support officially ended with `2.80`. See [the announcement](https://lists.blender.org/pipermail/bf-committers/2019-August/050124.html)

## Gotchas

Some unique hardware and software configurations may not work, and there is no extant list of things that don't work in the Python standalone module.
