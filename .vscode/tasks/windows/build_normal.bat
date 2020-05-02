del /F /s /q build\*.*
rmdir /s /q build
.\venv\3.7-32\Scripts\python bpy_setup.py bdist_wheel > logs\3.7-32_normal_build.log 2>&1
.\venv\3.7-64\Scripts\python bpy_setup.py sdist bdist_wheel > logs\3.7-64_normal_build.log 2>&1