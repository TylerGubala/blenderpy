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
yum install -y boost boost-devel fftw-devel freetype freetype-devel giflib glew glew-devel ilmbase ilmbase-devel jemalloc libX11-devel libXxf86vm-devel libXcursor-devel libXi-devel libXrandr-devel libXinerama-devel libjpeg-devel libpng-devel libsndfile libtiff libtiff-devel mesa-libGL mesa-libGL-devel SDL SDL_image tbb tbb-devel zlib zlib-devel openssl-devel bzip2-devel libffi-devel yasm

yum erase -y cmake

curl -L https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz -o Python-3.7.7.tgz
tar xzf Python-3.7.7.tgz
cd Python-3.7.7
./configure --enable-optimizations >> python_install.log
make install >> python_install.log
cd ..

curl -L https://www.libraw.org/data/LibRaw-0.19.5.tar.gz -o LibRaw-0.19.5.tar.gz
tar xzf LibRaw-0.19.5.tar.gz
cd LibRaw-0.19.5
./configure >> libraw_install.log
make >> libraw_install.log
make install >> libraw_install.log
cd ..

curl -O -L https://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2
tar xjf ffmpeg-snapshot.tar.bz2
cd ffmpeg
./configure --disable-x86asm >> ffmpeg_install.log
make -s >> ffmpeg_install.log
make install -s >> ffmpeg_install.log
cd ..

curl -L https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-1.12.0/src/hdf5-1.12.0.tar.gz -o hdf5-1.12.0.tar.gz
tar xzf hdf5-1.12.0.tar.gz
cd hdf5-1.12.0
./configure >> hdf5_install.log
make -s >> hdf5_install.log
make install -s >> hdf5_install.log
cd ..

curl -L https://github.com/Kitware/CMake/releases/download/v3.17.3/cmake-3.17.3-Linux-x86_64.tar.gz -o cmake-3.17.3-Linux-x86_64.tar.gz
tar xzf cmake-3.17.3-Linux-x86_64.tar.gz
PATH=$PATH:$(pwd)/cmake-3.17.3-Linux-x86_64/bin/

curl -L https://github.com/AcademySoftwareFoundation/openexr/tarball/v2.5.1 -o openexr-v2.5.1.tar.gz
tar xzf openexr-v2.5.1.tar.gz
cd AcademySoftwareFoundation-openexr-*
mkdir build
cd build
cmake .. >> openexr_install.log
make -s >> openexr_install.log
make install -s >> openexr_install.log
cd ../..

curl -L https://github.com/oneapi-src/oneTBB/releases/download/v2020.3/tbb-2020.3-lin.tgz -o tbb-2020.3-lin.tgz
tar xzf tbb-2020.3-lin.tgz
chmod u+x ./tbb/bin/tbbvars.sh
./tbb/bin/tbbvars.sh

git clone https://github.com/AcademySoftwareFoundation/openvdb.git
cd openvdb
mkdir build
cd build
cmake .. >> openvdb_install.log
make -s >> openvdb_install.log
make install -s >> openvdb_install.log
cd ../..

git clone https://github.com/uclouvain/openjpeg.git
cd openjpeg
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release >> openjpeg_install.log
make -s >> openjpeg_install.log
make install -s >> openjpeg_install.log
cd ../..

git clone -b release https://github.com/OpenImageIO/oiio.git
cd oiio
mkdir build
cd build
cmake .. >> openimageio_install.log
make -s >> openimageio_install.log
make install -s >> openimageio_install.log
cd ../..

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