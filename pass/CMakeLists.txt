# Copyright 2019 Vasily Rudchenko - Fuzzview
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Cmake file based on:
# https://github.com/abenkhadra/llvm-pass-tutorial

cmake_minimum_required(VERSION 3.13)
project(fvpass)

# SET(CMAKE_C_COMPILER $ENV{FV_LLVM_DIR}/bin/clang)
# SET(CMAKE_CXX_COMPILER $ENV{FV_LLVM_DIR}/bin/clang++)

# we need FV_LLVM_DIR in order not automatically set LLVM_DIR
if(NOT DEFINED ENV{FV_LLVM_DIR})
    message(FATAL_ERROR "$FV_LLVM_DIR is not defined")
else ()
    set(ENV{LLVM_DIR} $ENV{FV_LLVM_DIR}/lib/cmake/llvm)
endif()

find_package(LLVM REQUIRED CONFIG)
add_definitions(${LLVM_DEFINITIONS})
include_directories(${LLVM_INCLUDE_DIRS})
link_directories(${LLVM_LIBRARY_DIRS})

add_subdirectory(fvpass)
