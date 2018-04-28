# blenderpy
Blender as a python module with easy-install

## Installation

```py -m pip install blenderpy```

## How it works


### building: 

This is a setup.py file for easy installation of the blender python pyd or so file

Python starts by opening a temporary directory on the computer

Then, using Gitpython, this setup will download the git repository of blender into the temporary directory, along the way attempting to install dependencies

After downloading the files into ```TEMP_DIR/blender``` (where temp dir is the name of the temp directory) the program attempts to run the "make" command which exists inside the ```TEMP_DIR/blender``` directory.

```make bpy <OPTIONS>```

This will typically result in built files


### Installing after build

The blender python module expects all of the .dll files created (windows only) to be installed as siblings of the bpy.pyd file, so those must be in the same directory, and can be safely installed in site-packages

The resultant version folder (matches the version of blender) must be installed as a sibling of the executable file. You must put this folder as a sibling (in the same folder) of the python.exe that you are running from. In a venv, this is under the Scripts directory of the venv.

## Gotchas

I have not tested this for platforms other than windows at the moment. More to come soon.
