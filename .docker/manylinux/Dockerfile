FROM quay.io/pypa/manylinux2014_x86_64

WORKDIR /blenderpy

RUN yum install -y \
    alembic \
    blosc \
    blosc-devel \
    bzip2-devel \
    epel-release \
    fftw-devel \
    freetype \
    freetype-devel \
    gcc \
    gcc-c++ \
    giflib \
    giflib-devel \
    git \
    git-lfs \
    glew \
    glew-devel \
    glfw \
    glfw-devel \
    ilmbase \
    ilmbase-devel \
    jemalloc \
    jemalloc-devel \
    libffi-devel \
    libjpeg-devel \
    libjpeg-turbo \
    libjpeg-turbo-utils \
    libpng-devel \
    libsndfile \
    libsndfile-devel \
    libtiff \
    libtiff-devel \
    libwebp \
    libX11-devel \
    libXcursor-devel \
    libXi-devel \
    libXinerama-devel \
    libxml2-devel \
    libXrandr-devel \
    libXxf86vm-devel \
    make \
    mesa-libGL \
    mesa-libGL-devel \
    OpenColorIO \
    OpenColorIO-devel \
    OpenImageIO \
    OpenImageIO-devel \
    OpenImageIO-utils \
    openjpeg \
    openjpeg-libs \
    openssl-devel \
    python2 \
    python2-pip \
    python-devel \
    python-alembic \
    qt-devel \
    qt5-designer \
    qt5-qtbase \
    SDL \
    SDL_image \
    SDL2 \
    SDL2-devel \
    subversion \
    yasm \
    zlib \
    zlib-devel
RUN yum erase -y cmake

RUN yum localinstall -y --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm

RUN yum install -y ffmpeg ffmpeg-devel

RUN python2.7 -m pip install -U pip
RUN python2.7 -m pip install numpy

RUN curl -L https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz -o Python-3.7.7.tgz
RUN tar xzf Python-3.7.7.tgz
RUN cd Python-3.7.7 && \
    ./configure --enable-optimizations
RUN cd Python-3.7.7 && \
    make install
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

#RUN curl -O -L https://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2
#RUN tar xjf ffmpeg-snapshot.tar.bz2
#RUN cd ffmpeg && \
#    ./configure --disable-x86asm && \
#    make -s && \
#    make install -s
#RUN rm -Rf ffmpeg

RUN curl -L https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-1.12.0/src/hdf5-1.12.0.tar.gz -o hdf5-1.12.0.tar.gz
RUN tar xzf hdf5-1.12.0.tar.gz
RUN cd hdf5-1.12.0 && \
    ./configure && \
    make -s && \
    make install -s
RUN rm -Rf hdf5-1.12.0

RUN curl -L https://github.com/Kitware/CMake/releases/download/v3.17.3/cmake-3.17.3-Linux-x86_64.tar.gz -o cmake-3.17.3-Linux-x86_64.tar.gz
RUN tar xzf cmake-3.17.3-Linux-x86_64.tar.gz
ENV PATH="/blenderpy/cmake-3.17.3-Linux-x86_64/bin:${PATH}"

RUN curl -L https://github.com/AcademySoftwareFoundation/openexr/tarball/v2.5.1 -o openexr-v2.5.1.tar.gz
RUN tar xzf openexr-v2.5.1.tar.gz
RUN cd AcademySoftwareFoundation-openexr-* && \
    mkdir build && \
    cd build && \
    cmake .. && \
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
    cmake .. -DTBB_LIBRARYDIR=/opt/intel/tbb/lib/intel64/gcc4.8 -DTBB_INCLUDEDIR=/opt/intel/tbb/include && \
    make -s && \
    make install -s
RUN rm -Rf openvdb

RUN git clone https://github.com/uclouvain/openjpeg.git
RUN cd openjpeg && \
    mkdir build && \
    cd build &&\
    cmake .. -DCMAKE_BUILD_TYPE=Release && \
    make -s && \
    make install -s
RUN rm -Rf openjpeg

RUN curl -L https://github.com/ispc/ispc/releases/download/v1.12.0/ispc-v1.12.0b-linux.tar.gz -o ispc-v1.12.0b-linux.tar.gz
RUN tar xzf ispc-v1.12.0b-linux.tar.gz

RUN git lfs install
RUN git clone --recursive https://github.com/OpenImageDenoise/oidn.git
RUN cd oidn && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install
RUN rm -Rf oidn

RUN git clone https://github.com/KhronosGroup/OpenCOLLADA.git
RUN cd OpenCOLLADA && \
    mkdir build && \
    cd build && \
    ../../cmake-3.17.3-Linux-x86_64/bin/cmake .. && \
    make && \
    make install
RUN rm -Rf OpenCOLLADA

RUN git clone https://github.com/FreeSpacenav/spacenavd.git
RUN cd spacenavd && \
    ./configure && \
    make && \
    make install
RUN rm -Rf spacenavd

#Can't get these three to build

#RUN git clone https://github.com/imageworks/OpenShadingLanguage.git
#RUN cd OpenShadingLanguage && \
#    make
#RUN rm -Rf OpenShadingLanguage

#RUN git clone https://github.com/PixarAnimationStudios/USD
#RUN python USD/build_scripts/build_usd.py /usr/local/USD
#RUN rm -Rf USD

#RUN git clone https://github.com/PixarAnimationStudios/OpenSubdiv.git
#RUN cd OpenSubdiv && \
#    mkdir build && \
#    cd build && \
#    cmake -D NO_PTEX=1 -D NO_DOC=1 \
#      -D NO_OMP=1 -D NO_TBB=1 -D NO_CUDA=1 -D NO_OPENCL=1 -D NO_CLEW=1 \
#      -D GLFW_LOCATION="/usr/include/GLFW/" \
#      .. && \
#    cmake --build . --config Release --target install
#RUN rm -Rf OpenSubdiv

RUN yum install -y \
    tbb \
    tbb-devel
#Can't install tbb from old Centos using yum earlier otherwise we get "tbb version too low" error

COPY . /blenderpy

RUN /blenderpy/.docker/manylinux/build_manylinux_wheels.sh