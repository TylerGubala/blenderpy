#!/bin/bash
mkdir -p /Blender/lib
mkdir -p /Blender/build/linux
cd /Blender/build/linux
cmake ${1:-/Blender/blender} -DWITH_PYTHON_INSTALL=OFF -DWITH_PYTHON_MODULE=ON -DWITH_MEM_JEMALLOC=OFF -DWITH_CYCLES_CUDA_BINARIES=ON -DWITH_CYCLES_DEVICE_OPTIX=ON -DOPTIX_ROOT_DIR=/NVIDIA-OptiX-SDK-7.1.0-linux64-x86_64
make -j$((`nproc`+1)) install