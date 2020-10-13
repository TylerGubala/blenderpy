#!/bin/bash

if [ $TRAVIS_OS_NAME = 'osx' ]; then

    # Install some custom requirements on macOS

    brew install cmake git svn

    mkdir -p /Blender
    mkdir -p /build/osx

    cd /Blender

    git clone https://git.blender.org/blender.git

    cd blender

    ./make update

    cd /build/osx

    cmake /Blender/blender -DWITH_PYTHON_INSTALL=OFF -DWITH_PYTHON_MODULE=ON
    
elif [ $TRAVIS_OS_NAME = 'linux' ]; then

    # Install linux based dependencies

fi