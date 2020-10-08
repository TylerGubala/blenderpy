#!/usr/bin/bash
set -e -u -x

function repair_wheel {
    wheel="$1"
    if ! auditwheel show "$wheel"; then
        echo "Skipping non-platform wheel $wheel"
    else
        auditwheel repair "$wheel" --plat "$PLAT" -w /blenderpy/wheelhouse/
    fi
}

# Compile wheels
for PYBIN in /opt/python/cp37*/bin; do
    "${PYBIN}/pip" install -U pip
    "${PYBIN}/pip" install -r /blenderpy/requirements.txt
    "${PYBIN}/pip" wheel /blenderpy --no-deps -v -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    repair_wheel "$whl"
done