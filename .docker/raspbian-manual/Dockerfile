FROM arm32v5/debian:buster-20200803

WORKDIR /blenderpy

RUN apt-get -y install cmake g++ gcc git make libx11-dev libxxf86vm-dev libxcursor-dev libxi-dev libxrandr-dev libxinerama-dev subversion

# As of v2.80, 32 bit is no longer supported
# See https://developer.blender.org/T67184
RUN git clone -b v2.79 https://git.blender.org/blender.git
RUN svn checkout https://svn.blender.org/svnroot/bf-blender/tags/blender-2.79-release/lib/

RUN mkdir build && \
    cd build && \
    cmake ../blender -DWITH_MEM_JEMALLOC=OFF && \
    make update && \
    make && \
    make install