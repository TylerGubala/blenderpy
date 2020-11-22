#!/usr/bin/bash
set -e -u -x

function repair_wheel {
    wheel="$1"
    if ! auditwheel show "$wheel"; then
        echo "Skipping non-platform wheel $wheel"
    else
        auditwheel repair "$wheel" --plat manylinux2014_x86_64 -w /blenderpy/wheelhouse/
    fi
}

# Compile wheels
for PYBIN in /opt/python/cp37*/bin; do
# to install, uncomment the below line
#    "${PYBIN}/pip" install /blenderpy --global-option="build_ext" --global-option="--bpy-prebuilt=/build/linux/bin/" -v
    "${PYBIN}/pip" wheel /blenderpy --build-option="--bpy-prebuilt=/Blender/build/linux/bin/" --no-deps -v -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    repair_wheel "$whl"
    rm "$whl"
done

for whl in /blenderpy/wheelhouse/*.whl; do
    cp "$whl" /blenderpy/dist/
done