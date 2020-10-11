#/bin/bash
mkdir .blenderpy
mkdir .blenderpy/${1:-master}
cd .blenderpy/${1:-master}
git clone http://git.blender.org/blender.git -b ${1:-master}
cd blender
git submodule update --remote
git submodule update --init --recursive
git submodule foreach git checkout master
git submodule foreach git pull --rebase origin master
case "$3" in
  "--precompiled-libs")
    svn checkout https://svn.blender.org/svnroot/bf-blender/trunk/lib/linux_centos7_x86_64
    ;;
  "--compile-libs")
    ./build_files/build_environment/install_deps.sh
    ;;
  *)
    echo No library build method specified, skipping library retrieval
    ;;
esac
make update
cd ..
mkdir build_linux_bpy_custom
cd build_linux_bpy_custom

cmake ../blender -DWITH_AUDASPACE=OFF -DWITH_PYTHON_INSTALL=OFF -DWITH_PYTHON_MODULE=ON

make install -j$(nproc) | tee ../build_linux_bpy_custom_build.log

mkdir ../build_linux_bpy_custom_test

${2:-python3.7} -m venv ../build_linux_bpy_custom_test/venv

cp bin/bpy.so ../build_linux_bpy_custom_test/venv/lib/${2:-python3.7}/site-packages
find bin -maxdepth 1 -type d -exec cp -R {} ../build_linux_bpy_custom_test/venv/lib/${2:-python3.7}/site-packages \;

../build_linux_bpy_custom_test/venv/bin/${2:-python3.7} -c "import bpy; bpy.ops.render.render(write_still=True)" | tee ../build_linux_bpy_custom_test.log