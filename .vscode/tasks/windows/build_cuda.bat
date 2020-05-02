del /F /s /q build\*.*
rmdir /s /q build
.\venv\3.7-32\Scripts\python bpy_cuda_setup.py bdist_wheel > logs\3.7-32_cuda_build.log 2>&1
.\venv\3.7-64\Scripts\python bpy_cuda_setup.py sdist bdist_wheel > logs\3.7-64_cuda_build.log 2>&1