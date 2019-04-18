# Based on:
# https://github.com/abenkhadra/llvm-pass-tutorial
# commit 29481466d7c1b3e71c08f0013500534b3a8ed6c7

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
