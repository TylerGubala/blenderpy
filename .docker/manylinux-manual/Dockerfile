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

RUN curl -L https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz -o Python-3.7.7.tgz
RUN tar xzf Python-3.7.7.tgz
RUN cd Python-3.7.7 && \
    ./configure --enable-optimizations && \
    make install >> python_install.log
RUN rm -Rf Python-3.7.7

RUN curl -L https://github.com/Kitware/CMake/releases/download/v3.17.3/cmake-3.17.3-Linux-x86_64.tar.gz -o cmake-3.17.3-Linux-x86_64.tar.gz
RUN tar xzf cmake-3.17.3-Linux-x86_64.tar.gz
ENV PATH="/blenderpy/cmake-3.17.3-Linux-x86_64/bin:${PATH}"

RUN git clone https://git.blender.org/blender.git
RUN cd blender && \
    git checkout tags/v2.82 -b master

RUN mkdir lib
RUN cd lib && \
    svn checkout https://svn.blender.org/svnroot/bf-blender/tags/blender-2.82-release/lib/linux_centos7_x86_64

RUN cd blender && \
    make update
RUN cd blender && \
    make bpy