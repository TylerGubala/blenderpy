if [ -f setup.py ]; then
    rm setup.py
fi
cp "bpy/setup.py" .
rm -Rf build
./venv/3.5-32/bin/python3 setup.py bdist_wheel > logs/3.5-32_build.log 2>&1
./venv/3.5-64/bin/python3 setup.py sdist bdist_wheel > logs/3.5-64_build.log 2>&1
if [ -f setup.py ]; then
    rm setup.py
fi