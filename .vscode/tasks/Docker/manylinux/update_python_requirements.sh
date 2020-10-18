for PYBIN in /opt/python/*/bin; do
    "${PYBIN}/pip" install -U pip
    "${PYBIN}/pip" install -r /blenderpy/requirements.txt
done