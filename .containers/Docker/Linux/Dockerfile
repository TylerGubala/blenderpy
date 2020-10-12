FROM quay.io/pypa/manylinux2014_x86_64 AS builder

RUN yum-config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel7/x86_64/cuda-rhel7.repo && \
    yum -y clean all

RUN yum -y install \
    centos-release-scl \
    cuda-toolkit-10-1.x86_64  \
    gcc \
    gcc-c++ \
    glew-devel \
    libffi-devel \
    libX11-devel \
    libXcursor-devel \
    libXi-devel \
    libXinerama-devel \
    libxml2-devel \
    libXrandr-devel \
    make \
    openssl-devel && \
    yum -y clean all
RUN yum -y install devtoolset-7 && \
    yum -y clean all
# installs to /opt/rh/devtoolset-7/root/bin/gcc
# NVIDIA needs gcc < 8 since CUDA version is 10
RUN ln -sf /opt/rh/devtoolset-7/root/bin/gcc /usr/local/cuda/bin/gcc

ADD https://github.com/Kitware/CMake/releases/download/v3.17.3/cmake-3.17.3-Linux-x86_64.tar.gz cmake-3.17.3-Linux-x86_64.tar.gz
RUN tar xzf cmake-3.17.3-Linux-x86_64.tar.gz
ENV PATH="/blenderpy/cmake-3.17.3-Linux-x86_64/bin:${PATH}"

COPY . /blenderpy

RUN /blenderpy/Optix/NVIDIA-OptiX-SDK-7.1.0-linux64-x86_64.sh --include-subdir --skip-license

FROM centos:centos8 AS blenderpy-centos

RUN yum -y install python3.7

COPY --from=builder /blenderpy/wheelhouse/bpy-2.91-cp37-cp37m-manylinux2014_x86_64.whl .

RUN python3 -m pip install -U pip setuptools wheel
RUN python3 -m pip install bpy-2.91-cp37-cp37m-manylinux2014_x86_64.whl

CMD python3 -c "import bpy;print(dir(bpy.types));"

FROM debian:sid-20200803 AS blenderpy-debian

RUN apt-get -y install python3.7

COPY --from=builder /blenderpy/wheelhouse/bpy-2.91-cp37-cp37m-manylinux2014_x86_64.whl .

RUN python3 -m pip install -U pip setuptools wheel
RUN python3 -m pip install bpy-2.91-cp37-cp37m-manylinux2014_x86_64.whl

CMD python3 -c "import bpy;print(dir(bpy.types));"

FROM fedora:rawhide AS blenderpy-fedora

RUN dnf -y install python3.7

COPY --from=builder /blenderpy/wheelhouse/bpy-2.91-cp37-cp37m-manylinux2014_x86_64.whl .

RUN python3 -m pip install -U pip setuptools wheel
RUN python3 -m pip install bpy-2.91-cp37-cp37m-manylinux2014_x86_64.whl

CMD python3 -c "import bpy;print(dir(bpy.types));"

FROM ubuntu:groovy-20200812 AS blenderpy-ubuntu

RUN apt-get -y install python3.7

COPY --from=builder /blenderpy/wheelhouse/bpy-2.91-cp37-cp37m-manylinux2014_x86_64.whl .

RUN python3 -m pip install -U pip setuptools wheel
RUN python3 -m pip install bpy-2.91-cp37-cp37m-manylinux2014_x86_64.whl

CMD python3 -c "import bpy;print(dir(bpy.types));"