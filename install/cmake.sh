#!/bin/bash

cmake --version
apt remove cmake

cd $HOME
wget https://github.com/Kitware/CMake/releases/download/v3.14.0/cmake-3.14.0-Linux-x86_64.sh
chmod +x cmake-3.14.0-Linux-x86_64.sh
bash cmake-3.14.0-Linux-x86_64.sh --prefix=/usr/local --skip-license
rm cmake-3.14.0-Linux-x86_64.sh
cmake --version
