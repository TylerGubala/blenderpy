# blenderpy
Blender as a python module with easy-install

## Installation

```py -m pip install bpy```

## How it works


### building: 

This is a setup.py file for easy installation of the blender python pyd or so file

Python starts by opening a directory on the computer in the user's home folder (```~/blenderpy```)

Then, using Gitpython, this setup will download the git repository of blender into the directory, along the way attempting to install dependencies (such as cmake, svn and GitPython which are transient dependencies)

After downloading the files into ```~/.blenderpy``` the program attempts to walk you through the build process for blender. Results are created in the ```~/.blenderpy/build``` directory.

It does this by going and making sure that the VC build tools are installed, and then crawling the registry for the best build tool to use. Usually we are just able to use the generator for Windows 2017.

### Installing after build

The blender python module expects all of the .dll files created (windows only) to be installed as siblings of the bpy.pyd file, so those must be in the same directory, and can be safely installed in site-packages. A directory reflecting the version of the bpy module can also be found as a sibling of the python executible your environment is running in.

The resultant version folder (matches the version of blender) must be installed as a sibling of the executable file. You must put this folder as a sibling (in the same folder) of the python.exe that you are running from. In a venv, this is under the Scripts directory of the venv.

## Gotchas

I have not tested this for platforms other than windows at the moment. More to come soon.
