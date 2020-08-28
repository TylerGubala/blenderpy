FROM debian:sid-20200803

WORKDIR /blenderpy

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update
RUN apt-get -y install \
    build-essential \
    cmake \
    curl \
    g++ \
    gcc \
    git \
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
    ./configure --enable-optimizations && \
    make install

RUN python3.7 -m pip install -U pip
RUN python3.7 -m pip install wheel

COPY . /blenderpy

RUN cp /blenderpy/bpy/setup.py /blenderpy
RUN python3.7 setup.py