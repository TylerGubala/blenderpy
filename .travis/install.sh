#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then

    # Install some custom requirements on OS X
    brew install python

    case "${TOXENV}" in
        py34)
            # Install some custom Python 3.4 requirements on OS X
            echo
            ;;
        py35)
            # Install some custom Python 3.5 requirements on OS X
            echo
            ;;
        py36)
            # Install some custom Python 3.6 requirements on OS X
            echo
            ;;
        py37)
            # Install some custom Python 3.7 requirements on OS X
            echo
            ;;
    esac
else
    # Install some custom requirements on Linux
    echo
fi
python3 setup.py install