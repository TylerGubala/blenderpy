FROM debian:buster-20200803

WORKDIR /blenderpy

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update
RUN apt-get -y install build-essential cmake curl git libx11-dev libxxf86vm-dev libxcursor-dev libxi-dev libxrandr-dev libxinerama-dev libglew-dev subversion

ADD https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz Python-3.7.7.tgz
RUN tar xzf Python-3.7.7.tgz
RUN cd Python-3.7.7 && \
    ./configure --enable-optimizations && \
    make install

RUN git clone https://git.blender.org/blender.git
RUN cd blender &&\
    git checkout tags/v2.82 -b origin/master
RUN svn checkout https://svn.blender.org/svnroot/bf-blender/tags/blender-2.82-release/lib

RUN cd blender && \
    make update && \
    make bpy