FROM quay.io/pypa/manylinux2014_x86_64

WORKDIR /blenderpy

RUN yum install -y \
    gcc \
    gcc-c++ \
    git \
    git-lfs \
    glew-devel \
    libffi-devel \
    libX11-devel \
    libXcursor-devel \
    libXi-devel \
    libXinerama-devel \
    libxml2-devel \
    libXrandr-devel \
    make \
    openssl-devel \
    subversion

RUN curl -L https://github.com/Kitware/CMake/releases/download/v3.17.3/cmake-3.17.3-Linux-x86_64.tar.gz -o cmake-3.17.3-Linux-x86_64.tar.gz
RUN tar xzf cmake-3.17.3-Linux-x86_64.tar.gz
ENV PATH="/blenderpy/cmake-3.17.3-Linux-x86_64/bin:${PATH}"

RUN /blenderpy/.docker/manylinux/build_manylinux_wheels.sh