FROM fedora:rawhide

WORKDIR /blenderpy

RUN sudo dnf -y update
RUN sudo dnf -y install cmake gcc gcc-c++ git glew-devel libX11-devel libXi-devel libXcursor-devel libXrandr-devel libXinerama-devel libstdc++-static make subversion

RUN curl -L https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz -o Python-3.7.7.tgz
RUN tar xzf Python-3.7.7.tgz
RUN cd Python-3.7.7 && \
    ./configure --enable-optimizations && \
    make install >> python_install.log
RUN rm -Rf Python-3.7.7

RUN python3.7 -m pip install -U pip
RUN python3.7 -m pip install wheel

COPY . /blenderpy

RUN cp /blenderpy/bpy/setup.py /blenderpy
RUN python3.7 setup.py