# blenderpy
Blender as a python module with easy-install

Meant for installation into a virtualenv or wherever, for unit testing of Blender extensions being authored, or developement of a Blender 3d-enabled Python application.

Depends upon the `bpy-build` and `bpy-ensure` modules to make sure the Blender `bpy` module environment is correct.

For more information, please see:

[bpy-build repository](https://github.com/TylerGubala/bpy-build)

[bpy-ensure repository](https://github.com/TylerGubala/bpy-ensure)

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

A. More work is being done in `bpy-make`, another repo. In there, we search for the appropriate Python/OS combination based on what we know about the currently running executable, but it's far from perfect, and is WIP. Help is needed in handling `svn` repo traversal.

## Gotchas

I have not tested this for platforms other than Windows Python 3.6.x at the moment. More to come soon.

## Support this project

By supporting this project you are validating the time, mental effort and computer downtime that I face when providing wheels for this project. Thanks in advance for any donation you give, no matter how small.

<a href="https://www.patreon.com/bePatron?u=3979551" data-patreon-widget-type="become-patron-button"><img src="https://cloakandmeeple.files.wordpress.com/2017/06/become_a_patron_button3x.png?w=610" width="180px"></a>

[![Support via PayPal](https://cdn.rawgit.com/twolfson/paypal-github-button/1.0.0/dist/button.svg)](https://www.paypal.me/tylergubala/)
