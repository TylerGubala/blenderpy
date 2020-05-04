if exist setup.py del setup.py
copy "bpy-optix\setup.py" .
del /F /s /q build\*.*
rmdir /s /q build
.\venv\3.7-32\Scripts\python setup.py bdist_wheel > logs\3.7-32_optix_build.log 2>&1
.\venv\3.7-64\Scripts\python setup.py sdist bdist_wheel > logs\3.7-64_optix_build.log 2>&1
if exist setup.py del setup.py