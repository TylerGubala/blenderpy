FROM fedora:rawhide

RUN sudo dnf -y update
RUN sudo dnf -y install gcc gcc-c++ git subversion make cmake libX11-devel libXi-devel libXcursor-devel libXrandr-devel libXinerama-devel libstdc++-static python3.7

RUN python3 -m pip install -U pip

COPY . /blenderpy

CMD [ "/blenderpy/.docker/windows/install.bat" ]