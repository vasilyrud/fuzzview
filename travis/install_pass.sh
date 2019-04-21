#!/bin/bash

cd $TRAVIS_BUILD_DIR/fuzzview/pass
mkdir build
cd $TRAVIS_BUILD_DIR/fuzzview/pass/build
cmake ..
make
