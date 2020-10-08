FROM quay.io/pypa/manylinux2014_x86_64 AS builder

WORKDIR /blenderpy

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
RUN ln -sf /opt/rh/devtoolset-7/root/bin/gcc /usr/local/cuda/bin/gcc

ADD https://github.com/Kitware/CMake/releases/download/v3.17.3/cmake-3.17.3-Linux-x86_64.tar.gz cmake-3.17.3-Linux-x86_64.tar.gz
RUN tar xzf cmake-3.17.3-Linux-x86_64.tar.gz
ENV PATH="/blenderpy/cmake-3.17.3-Linux-x86_64/bin:${PATH}"

COPY . /blenderpy

RUN Optix/NVIDIA-OptiX-SDK-7.1.0-linux64-x86_64.sh --include-subdir --skip-license

RUN mkdir build_linux_bpy
RUN cd build_linux_bpy && \
    cmake ../Blender/blender -DWITH_PYTHON_INSTALL=OFF -DWITH_PYTHON_MODULE=ON -DWITH_CYCLES_CUDA_BINARIES=ON -DWITH_CYCLES_DEVICE_OPTIX=ON -DOPTIX_ROOT_DIR=/blenderpy/NVIDIA-OptiX-SDK-7.1.0-linux64/SDK
RUN cd build_linux_bpy && \
    make install

RUN /blenderpy/.vscode/tasks/unix/build_manylinux_wheels.sh

FROM centos:centos8 AS blenderpy-centos

WORKDIR /blenderpy

RUN yum -y install python3.7

COPY --from=builder /blenderpy/build_linux_bpy/bin/bpy.so /usr/local/lib/python3.7/site-packages
COPY --from=builder /blenderpy/lib/linux_centos7_x86_64/python/lib/python3.7/site-packages/2.91 /usr/local/lib/python3.7/site-packages/

CMD python3 -c "import bpy;print(dir(bpy.types));"

FROM debian:sid-20200803 AS blenderpy-debian

WORKDIR /blenderpy

RUN apt-get -y install python3.7

COPY --from=builder /blenderpy/build_linux_bpy/bin/bpy.so /usr/local/lib/python3.7/site-packages
COPY --from=builder /blenderpy/lib/linux_centos7_x86_64/python/lib/python3.7/site-packages/2.91 /usr/local/lib/python3.7/site-packages/

CMD python3 -c "import bpy;print(dir(bpy.types));"

FROM fedora:rawhide AS blenderpy-fedora

WORKDIR /blenderpy

RUN dnf -y install python3.7

COPY --from=builder /blenderpy/build_linux_bpy/bin/bpy.so /usr/local/lib/python3.7/site-packages
COPY --from=builder /blenderpy/lib/linux_centos7_x86_64/python/lib/python3.7/site-packages/2.91 /usr/local/lib/python3.7/site-packages/

CMD python3 -c "import bpy;print(dir(bpy.types));"

FROM ubuntu:groovy-20200812 AS blenderpy-ubuntu

WORKDIR /blenderpy

RUN apt-get -y install python3.7

COPY --from=builder /blenderpy/build_linux_bpy/bin/bpy.so /usr/local/lib/python3.7/site-packages
COPY --from=builder /blenderpy/lib/linux_centos7_x86_64/python/lib/python3.7/site-packages/2.91 /usr/local/lib/python3.7/site-packages/

CMD python3 -c "import bpy;print(dir(bpy.types));"

FROM winamd64/python:3.7.9-windowsservercore-1809 AS blenderpy-windows

WORKDIR /blenderpy

# Restore the default Windows shell for correct batch processing.
SHELL ["cmd", "/S", "/C"]

# Download the Build Tools bootstrapper.
ADD https://aka.ms/vs/16/release/vs_buildtools.exe vs_buildtools.exe

# Install Build Tools with the Microsoft.VisualStudio.Workload.AzureBuildTools workload, excluding workloads and components with known issues.
RUN vs_buildtools.exe --quiet --wait --norestart --nocache \
    --installPath "C:\BuildTools" \
    --add Microsoft.VisualStudio.Workload.AzureBuildTools \
    --remove Microsoft.VisualStudio.Component.Windows10SDK.10240 \
    --remove Microsoft.VisualStudio.Component.Windows10SDK.10586 \
    --remove Microsoft.VisualStudio.Component.Windows10SDK.14393 \
    --remove Microsoft.VisualStudio.Component.Windows81SDK \
 || IF "%ERRORLEVEL%"=="3010" EXIT 0

ADD https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz Python-3.7.7.tgz
RUN tar xzf Python-3.7.7.tgz
RUN cd Python-3.7.7 && \
    ./configure --enable-optimizations
RUN cd Python-3.7.7 && \
    make install

RUN py -m pip install -U pip

COPY . /blenderpy

RUN py -m pip install -r requirements.txt
RUN cp /blenderpy/bpy/setup.py /blenderpy
RUN py -m pip install . -v

CMD py -c "import bpy"