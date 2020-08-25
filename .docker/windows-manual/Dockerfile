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

RUN git clone https://git.blender.org/blender.git
RUN cd blender && \
    git checkout tags/v2.82 -b origin/master
RUN svn checkout https://svn.blender.org/svnroot/bf-blender/tags/blender-2.82-release/lib

RUN cd blender && \
    make update && \
    make bpy