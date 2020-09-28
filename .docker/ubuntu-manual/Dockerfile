FROM ubuntu:groovy-20200812

WORKDIR /blenderpy

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update
RUN apt-get -y install \
    build-essential \
    cmake \
    curl \
    git \
    libffi-dev \
    libssl-dev \
    libx11-dev \
    libxxf86vm-dev \
    libxcursor-dev \
    libxi-dev \
    libxrandr-dev \
    libxinerama-dev \
    libglew-dev \
    subversion \
    zlib1g-dev

ADD https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz Python-3.7.7.tgz
RUN tar xzf Python-3.7.7.tgz
RUN cd Python-3.7.7 && \
    ./configure --enable-optimizations
RUN cd Python-3.7.7 && \
    make install

RUN git clone https://git.blender.org/blender.git
RUN cd blender && \
    git checkout tags/v2.90.0 -b origin/master

RUN mkdir lib
RUN cd lib && \
    svn checkout https://svn.blender.org/svnroot/bf-blender/tags/blender-2.90-release/lib/linux_centos7_x86_64

RUN cd blender && \
    git submodule update --init --recursive
RUN cd blender && \
    make bpy
	
RUN cp /blenderpy/build_linux_bpy/bin/bpy.so /usr/local/lib/python3.7/site-packages
RUN mv /blenderpy/lib/linux_centos7_x86_64/python/lib/python3.7/site-packages/2.91 /usr/local/lib/python3.7/site-packages/
	
CMD python3 -c "import bpy;print(dir(bpy.types));"