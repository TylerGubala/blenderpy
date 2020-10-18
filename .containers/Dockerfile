FROM quay.io/pypa/manylinux2014_x86_64 AS blenderpy-manylinux-wheel-builder

RUN yum-config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel7/x86_64/cuda-rhel7.repo && \
    yum -y clean all

RUN yum -y install \
    centos-release-scl \
    cuda-toolkit-10-1.x86_64  \
    gcc \
    gcc-c++ \
    git \
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
    subversion && \
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

RUN /blenderpy/.vscode/tasks/Docker/manylinux/update_python_requirements.sh

FROM winamd64/python:3.7.9-windowsservercore-1809 AS blenderpy-windows-wheel-builder

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