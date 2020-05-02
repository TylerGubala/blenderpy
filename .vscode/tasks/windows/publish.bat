.\venv\3.7-64\Scripts\twine.exe upload dist/*
del /F /s /q build\*.*
rmdir /s /q build
del /s /q dist\*.*