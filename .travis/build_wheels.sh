#!/bin/bash
set -e -u -x

function repair_wheel {
    wheel="$1"
    if ! auditwheel show "$wheel"; then
        echo "Skipping non-platform wheel $wheel"
    else
        auditwheel repair "$wheel" --plat "$PLAT" -w /io/wheelhouse/
    fi
}

yum install -y gcc gcc-c++ make
yum install -y git subversion
yum install -y boost boost-devel fftw-devel freetype freetype-devel glew glew-devel jemalloc libX11-devel libXxf86vm-devel libXcursor-devel libXi-devel libXrandr-devel libXinerama-devel libjpeg-devel libpng-devel libosl libsndfile mesa-libGL OpenEXR OpenEXR-devel SDL SDL_image libSDL_image zlib zlib-devel openssl-devel bzip2-devel libffi-devel

yum erase -y cmake python

curl -L https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz -o Python-3.7.7.tgz
tar xzf Python-3.7.7.tgz
cd Python-3.7.7
./configure --enable-optimizations
make install
cd ..

curl -L https://github.com/Kitware/CMake/releases/download/v3.17.3/cmake-3.17.3-Linux-x86_64.tar.gz -o cmake-3.17.3-Linux-x86_64.tar.gz
tar xvzf cmake-3.17.3-Linux-x86_64.tar.gz

PATH=$PATH:cmake-3.17.3-Linux-x86_64/bin

# Compile wheels
for PYBIN in /opt/python/cp37*/bin; do
    PATH=$PATH:${PYBIN}
    "${PYBIN}/pip" install -r /io/requirements.txt
    cp /io/bpy/setup.py /io/setup.py
    "${PYBIN}/pip" wheel /io/ --no-deps -w wheelhouse/
    rm /io/setup.py
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    repair_wheel "$whl"
done

# Install packages and test
for PYBIN in /opt/python/*/bin/; do
    "${PYBIN}/pip" install python-manylinux-demo --no-index -f /io/wheelhouse
    (cd "$HOME"; "${PYBIN}/nosetests" pymanylinuxdemo)
done