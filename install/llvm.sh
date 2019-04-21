#!/bin/bash

cd $HOME
mkdir -p llvm/701

cd $HOME/llvm/701
wget http://releases.llvm.org/7.0.1/clang+llvm-7.0.1-x86_64-linux-gnu-ubuntu-16.04.tar.xz
tar -xJf clang+llvm-7.0.1-x86_64-linux-gnu-ubuntu-16.04.tar.xz
rm clang+llvm-7.0.1-x86_64-linux-gnu-ubuntu-16.04.tar.xz
mv clang+llvm-7.0.1-x86_64-linux-gnu-ubuntu-16.04 bin
