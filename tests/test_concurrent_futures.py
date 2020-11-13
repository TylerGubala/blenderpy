#!/usr/bin/python
# -*- coding: utf-8 -*-
"""A basic example program that shows the `bpy` and `multiprocessing` fix

Compatibility between these two libraries is strained by `bpy`'s own
requirement to append its user and addon modules directories to the `sys.path`
as well as the presence of a module in the addons directory called `bpy`,
resulting in an ambiguity between the legitimate `bpy` Blender runtime module
and the addon module the Blender 3d application requires
"""
# STD LIB imports
import concurrent.futures
from multiprocessing import freeze_support # For NT python exe creation
import sys

def multiFunction(data):
    import bpy
    print(data)
    print(bpy)

if __name__ == '__main__' :

    freeze_support()

    data = ['Uno','Deux','Three']

    with concurrent.futures.ProcessPoolExecutor() as p:

        p.map(multiFunction,data)
