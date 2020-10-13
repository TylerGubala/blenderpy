#!/bin/bash

if [ $TRAVIS_OS_NAME = 'osx' ]; then

    # Install blenderpy on macOS

    cd /build/osx

    make install
    
elif [ $TRAVIS_OS_NAME = 'linux' ]; then

    # Install blenderpy on linux

fi