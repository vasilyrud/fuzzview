#!/bin/bash

cd $FV_DIR/pass
mkdir build

cd $FV_DIR/pass/build
cmake ..
make
