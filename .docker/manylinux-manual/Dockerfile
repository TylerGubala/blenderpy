FROM quay.io/pypa/manylinux2014_x86_64

WORKDIR /blenderpy

RUN yum install -y \
    gcc \
    gcc-c++ \
    git \
    git-lfs \
    libX11-devel \
    libXcursor-devel \
    libXi-devel \
    libXinerama-devel \
    libxml2-devel \
    libXrandr-devel \
    make \
    subversion

RUN curl -L https://github.com/Kitware/CMake/releases/download/v3.17.3/cmake-3.17.3-Linux-x86_64.tar.gz -o cmake-3.17.3-Linux-x86_64.tar.gz
RUN tar xzf cmake-3.17.3-Linux-x86_64.tar.gz
ENV PATH="/blenderpy/cmake-3.17.3-Linux-x86_64/bin:${PATH}"

RUN git clone https://git.blender.org/blender.git
RUN cd blender && \
    git checkout tags/v2.82
RUN svn checkout https://svn.blender.org/svnroot/bf-blender/tags/blender-2.82-release/lib

RUN cd blender && \
    make update && \
    make bpy