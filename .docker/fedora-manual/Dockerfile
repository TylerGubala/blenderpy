FROM fedora:rawhide

WORKDIR /blenderpy

RUN sudo dnf -y update
RUN sudo dnf -y install cmake findutils gcc gcc-c++ git glew-devel libX11-devel libXi-devel libXcursor-devel libXrandr-devel libXinerama-devel libXxf86vm-devel libstdc++-static make subversion zlib-devel

ADD https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz Python-3.7.7.tgz
RUN tar xzf Python-3.7.7.tgz
RUN cd Python-3.7.7 && \
    ./configure --enable-optimizations && \
    make install

RUN git clone https://git.blender.org/blender.git

RUN mkdir lib
RUN cd lib && \
    svn checkout https://svn.blender.org/svnroot/bf-blender/trunk/lib/linux_centos7_x86_64

RUN cd blender && \
    make update
RUN cd blender && \
    make bpy
	
RUN cp /blenderpy/build_linux_bpy/bin/bpy.so /usr/local/lib/python3.7/site-packages
RUN mv /blenderpy/lib/linux_centos7_x86_64/python/lib/python3.7/site-packages/2.91 /usr/local/lib/python3.7/site-packages/
	
CMD python3 -c "import bpy;print(dir(bpy.types));"