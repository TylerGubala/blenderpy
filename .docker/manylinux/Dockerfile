FROM quay.io/pypa/manylinux2014_x86_64

WORKDIR /blenderpy

RUN yum install -y \
    make \
    blosc \
    blosc-devel \
    bzip2-devel \
    fftw-devel \
    freetype \
    freetype-devel \
    gcc \
    gcc-c++ \
    giflib \
    git \
    git-lfs \
    glew \
    glew-devel \
    ilmbase \
    ilmbase-devel \
    jemalloc \
    jemalloc-devel \
    libffi-devel \
    libjpeg-devel \
    libpng-devel \
    libsndfile \
    libtiff \
    libtiff-devel \
    libX11-devel \
    libXxf86vm-devel \
    libXcursor-devel \
    libXi-devel \
    libXrandr-devel \
    libXinerama-devel \
    mesa-libGL \
    mesa-libGL-devel \
    OpenImageIO \
    OpenImageIO-devel \
    OpenImageIO-utils \
    openssl-devel \
    python2 \
    python2-pip \
    python-devel \
    SDL \
    SDL_image \
    subversion \
    yasm \
    zlib \
    zlib-devel
RUN yum erase -y cmake

RUN python2.7 -m pip install -U pip
RUN python2.7 -m pip install numpy

RUN curl -L https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz -o Python-3.7.7.tgz
RUN tar xzf Python-3.7.7.tgz
RUN cd Python-3.7.7 && \
    ./configure --enable-optimizations && \
    make install >> python_install.log
RUN rm -Rf Python-3.7.7

RUN curl -L https://dl.bintray.com/boostorg/release/1.74.0/source/boost_1_74_0.tar.gz -o boost_1_74_0.tar.gz
RUN tar xzf boost_1_74_0.tar.gz
RUN cd boost_1_74_0 && \
    ./bootstrap.sh && \
    ./b2 install -q
RUN rm -Rf boost_1_74_0

RUN curl -L https://www.libraw.org/data/LibRaw-0.19.5.tar.gz -o LibRaw-0.19.5.tar.gz
RUN tar xzf LibRaw-0.19.5.tar.gz
RUN cd LibRaw-0.19.5 && \
    ./configure && \
    make && \
    make install
RUN rm -Rf LibRaw-0.19.5

RUN curl -O -L https://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2
RUN tar xjf ffmpeg-snapshot.tar.bz2
RUN cd ffmpeg && \
    ./configure --disable-x86asm && \
    make -s && \
    make install -s
RUN rm -Rf ffmpeg

RUN curl -L https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-1.12.0/src/hdf5-1.12.0.tar.gz -o hdf5-1.12.0.tar.gz
RUN tar xzf hdf5-1.12.0.tar.gz
RUN cd hdf5-1.12.0 && \
    ./configure && \
    make -s && \
    make install -s
RUN rm -Rf hdf5-1.12.0

RUN curl -L https://github.com/Kitware/CMake/releases/download/v3.17.3/cmake-3.17.3-Linux-x86_64.tar.gz -o cmake-3.17.3-Linux-x86_64.tar.gz
RUN tar xzf cmake-3.17.3-Linux-x86_64.tar.gz

RUN curl -L https://github.com/AcademySoftwareFoundation/openexr/tarball/v2.5.1 -o openexr-v2.5.1.tar.gz
RUN tar xzf openexr-v2.5.1.tar.gz
RUN cd AcademySoftwareFoundation-openexr-* && \
    mkdir build && \
    cd build && \
    ../../cmake-3.17.3-Linux-x86_64/bin/cmake .. && \
    make -s && \
    make install -s
RUN rm -Rf AcademySoftwareFoundation-openexr-*

RUN mkdir /opt/intel
RUN cd /opt/intel && \
    curl -L https://github.com/oneapi-src/oneTBB/releases/download/v2020.3/tbb-2020.3-lin.tgz -o tbb-2020.3-lin.tgz && \
    tar xzf tbb-2020.3-lin.tgz
RUN chmod u+x /opt/intel/tbb/bin/tbbvars.sh
RUN /opt/intel/tbb/bin/tbbvars.sh intel64 linux auto_tbbroot

RUN git clone https://github.com/AcademySoftwareFoundation/openvdb.git
RUN cd openvdb && \
    mkdir build && \
    cd build && \
    ../../cmake-3.17.3-Linux-x86_64/bin/cmake .. -DTBB_LIBRARYDIR=/opt/intel/tbb/lib/intel64/gcc4.8 -DTBB_INCLUDEDIR=/opt/intel/tbb/include && \
    make -s && \
    make install -s
RUN rm -Rf openvdb

RUN git clone https://github.com/uclouvain/openjpeg.git
RUN cd openjpeg && \
    mkdir build && \
    cd build &&\
    ../../cmake-3.17.3-Linux-x86_64/bin/cmake .. -DCMAKE_BUILD_TYPE=Release && \
    make -s && \
    make install -s
RUN rm -Rf openjpeg

RUN curl -L https://github.com/ispc/ispc/releases/download/v1.12.0/ispc-v1.12.0b-linux.tar.gz -o ispc-v1.12.0b-linux.tar.gz
RUN tar xzf ispc-v1.12.0b-linux.tar.gz

RUN git clone --recursive https://github.com/OpenImageDenoise/oidn.git
RUN cd oidn && \
    mkdir build && \
    cd build && \
    ../../cmake-3.17.3-Linux-x86_64/bin/cmake .. && \
    make
RUN rm -Rf oidn

COPY . /blenderpy

CMD [ "/blenderpy/.travis/install.sh" ]