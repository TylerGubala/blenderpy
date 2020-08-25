FROM arm32v5/debian:buster-20200803

WORKDIR /blenderpy

RUN apt-get -y install cmake g++ gcc git make libx11-dev libxxf86vm-dev libxcursor-dev libxi-dev libxrandr-dev libxinerama-dev subversion

ADD https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz Python-3.7.7.tgz
RUN tar xzf Python-3.7.7.tgz
RUN cd Python-3.7.7 && \
    ./configure --enable-optimizations && \
    make install

RUN git clone https://git.blender.org/blender.git
# As of v2.80, 32 bit is no longer supported
# See https://developer.blender.org/T67184
RUN cd blender && \
    git checkout tags/v2.79 -b origin/master

RUN mkdir lib
RUN cd lib && \
    svn checkout https://svn.blender.org/svnroot/bf-blender/blender-2.79-release/lib/linux_centos7_x86_64

RUN cd blender && \
    make update
RUN cd blender && \
    make bpy