if exist setup.py del setup.py
copy "bpy\setup.py" .
del /F /s /q build\*.*
rmdir /s /q build
.\venv\3.5-32\Scripts\python setup.py bdist_wheel > logs\3.5-32_normal_build.log 2>&1
.\venv\3.5-64\Scripts\python setup.py sdist bdist_wheel > logs\3.5-64_normal_build.log 2>&1
if exist setup.py del setup.py