#!/bin/bash

echo $PATH

cd $TRAVIS_BUILD_DIR/pass
mkdir build
cd $TRAVIS_BUILD_DIR/pass/build
cmake ..
make
