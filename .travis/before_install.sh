#!/bin/bash

if [ $TRAVIS_OS_NAME = 'osx' ]; then

    # Install some custom requirements on macOS

    brew install cmake git svn

    mkdir -p /build/darwin

    cd /Blender

    cd blender

    ./make update

    cd /build/darwin

    cmake /Blender/blender -DWITH_PYTHON_INSTALL=OFF -DWITH_PYTHON_MODULE=ON -DWITH_MEM_JEMALLOC=OFF
    
elif [ $TRAVIS_OS_NAME = 'linux' ]; then

    # Install linux based dependencies

    echo linux not supported

fi