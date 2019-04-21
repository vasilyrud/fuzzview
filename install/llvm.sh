#!/bin/bash

# In case Travis CI cached this already
if [ -d "$HOME/llvm/701/bin" ]; then
    echo "Skipping LLVM build because ${HOME}/llvm/701/bin dir already exists."
    exit 0
fi

cd $HOME
mkdir -p llvm/701

cd $HOME/llvm/701
wget http://releases.llvm.org/7.0.1/clang+llvm-7.0.1-x86_64-linux-gnu-ubuntu-16.04.tar.xz
tar -xJf clang+llvm-7.0.1-x86_64-linux-gnu-ubuntu-16.04.tar.xz

rm clang+llvm-7.0.1-x86_64-linux-gnu-ubuntu-16.04.tar.xz
mv clang+llvm-7.0.1-x86_64-linux-gnu-ubuntu-16.04 bin
