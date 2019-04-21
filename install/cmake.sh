#!/bin/bash

# To use:
# bash cmake.sh /path/to/install

cd $HOME
wget https://github.com/Kitware/CMake/releases/download/v3.14.0/cmake-3.14.0-Linux-x86_64.sh
chmod +x cmake-3.14.0-Linux-x86_64.sh

mkdir -p $1
bash cmake-3.14.0-Linux-x86_64.sh --prefix=$1 --skip-license

rm cmake-3.14.0-Linux-x86_64.sh
$1/bin/cmake --version
