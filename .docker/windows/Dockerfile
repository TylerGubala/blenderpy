FROM winamd64/python:3.7.9-windowsservercore-1809

WORKDIR /blenderpy

# Download the Build Tools bootstrapper.
ADD https://aka.ms/vs/16/release/vs_buildtools.exe C:\TEMP\vs_buildtools.exe

# Install Build Tools with the Microsoft.VisualStudio.Workload.AzureBuildTools workload, excluding workloads and components with known issues.
RUN C:\TEMP\vs_buildtools.exe --quiet --wait --norestart --nocache \
    --installPath C:\BuildTools \
    --add Microsoft.VisualStudio.Workload.AzureBuildTools \
    --remove Microsoft.VisualStudio.Component.Windows10SDK.10240 \
    --remove Microsoft.VisualStudio.Component.Windows10SDK.10586 \
    --remove Microsoft.VisualStudio.Component.Windows10SDK.14393 \
    --remove Microsoft.VisualStudio.Component.Windows81SDK \
 || IF "%ERRORLEVEL%"=="3010" EXIT 0

RUN py -m pip install -U pip

COPY . /blenderpy

RUN py -m pip install -r requirements.txt
RUN cp /blenderpy/bpy/setup.py /blenderpy
RUN py setup.py -v

CMD [ "py", "-c", '"import bpy"' ]