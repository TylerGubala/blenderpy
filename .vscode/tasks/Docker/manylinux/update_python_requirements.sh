for PYBIN in /opt/python/cp37*/bin; do
    "${PYBIN}/pip" install -U pip
    "${PYBIN}/pip" install -r /blenderpy/requirements.txt
done