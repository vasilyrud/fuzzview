#!/bin/bash

cd $TRAVIS_BUILD_DIR/pass
mkdir build
cd $TRAVIS_BUILD_DIR/pass/build
cmake ..
make
