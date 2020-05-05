# blenderpy
Blender as a python module with easy-install

## About

Meant for installation into a virtualenv or wherever, for unit testing of Blender extensions being authored, or developement of a Blender 3d-enabled Python application.

Depends upon the `bpy-build` module to make sure the Blender `bpy` module environment is correct.

For more information, please see:

[bpy-build repository](https://github.com/TylerGubala/bpy-build)

## Getting Started

Prebuilt wheels are provided for popular Platforms (MacOS, Windows, and Ubuntu). Prebuilds include "normal" installation (`bpy`), CUDA (`bpy-cuda`) and Optix (`bpy-optix`). Choosing the correct version depends on your use-case and hardware but in general `bpy` should be just fine for non-rendering automation tasks while `bpy-optix` has the best performance but requires a NVIDIA RTX Card and up to date drivers.

### Installing

Installing a prebuilt on these platforms is simple.

#### Windows

`py -m pip install bpy && bpy_post_install`

#### MacOS

`python3 -m pip install bpy && bpy_post_install`

#### Other

`python3 -m pip install bpy`

### Self Building

Building the Blender API for your own platform can be difficult, however this repo should make it easy enough for you to create your own builds by hand.

#### Build from `sdist`

You can build from a source distribution using `pip`.

##### Prerequisites

**Windows**
```bash
py -3.7-64 -m pip install --upgrade pip wheel future-fstrings
```

**Other**
```bash
python3.7 -m pip install --upgrade pip wheel future-fstrings
```

##### Build

**Windows**
```bash
py -3.7-64 -m pip install bpy --no-binary
```

**Other**
```bash
python3.7 -m pip install bpy --no-binary
```

#### Build from repo

You can also build after cloning the repository, this is helpful during development.

##### Prerequisites

```bash
python3 -m pip install --upgrade pip wheel future-fstrings
git clone https://github.com/TylerGubala/blenderpy.git
```

##### Build

If you have a specific version of `bpy` you want, you have to change the `VERSION` string at the beginning of the `bpy_<optional extra>_setup.py` file.

To build, run the below command.

**Windows**
`py bpy_setup.py sdist bdist_wheel`
**Other**
`python3 bpy_setup.py sdist bdist_wheel`

The resultant wheel in the dist folder can be installed using pip.

Post any errors you have as an issue.

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

A. [MacOS support is on its way](https://github.com/TylerGubala/blenderpy/wiki/Platform---MacoOS#build-script). After that is Ubuntu.

### Q. What about my Python version of choice?

A. Some builds you will have to make yourself if you have a specific version of the API you want. Likewise, if you are contrained to a specific Python version (especially those that aren't shipped by python.org) then you may have to try and build yourself.

## Gotchas

I have not tested this for platforms other than Windows Python 3.6.x at the moment. More to come soon.
