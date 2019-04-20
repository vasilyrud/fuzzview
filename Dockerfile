# syntax=docker/dockerfile:experimental

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

# To build:
# DOCKER_BUILDKIT=1 docker build -t fuzzview -f Dockerfile --ssh default=$SSH_AUTH_SOCK .
# export FV_DOCKER_CONTAINER=$(docker run -v $(PWD):/root/fuzzview -it -d fuzzview /bin/bash)
# docker exec -it $FV_DOCKER_CONTAINER bash

# Use raw Ubuntu as base
FROM ubuntu:16.04

# Install Ubuntu apps
RUN apt-get update && \
    apt-get -y install \
        build-essential \
        sudo \
        wget \
        less \
        nano \
        git \
        openssh-client \
        subversion \
        python3 \
        python3-pip \
        graphviz \
        tmux

# Install LLVM 7.0.1
WORKDIR /root
RUN mkdir -p llvm/701

WORKDIR /root/llvm/701
RUN wget http://releases.llvm.org/7.0.1/clang+llvm-7.0.1-x86_64-linux-gnu-ubuntu-16.04.tar.xz
RUN tar -xJf clang+llvm-7.0.1-x86_64-linux-gnu-ubuntu-16.04.tar.xz
RUN rm clang+llvm-7.0.1-x86_64-linux-gnu-ubuntu-16.04.tar.xz
RUN mv clang+llvm-7.0.1-x86_64-linux-gnu-ubuntu-16.04 bin
ENV FV_LLVM_DIR /root/llvm/701/bin

# Install cmake (newer version than that available with apt)
WORKDIR /root
RUN wget https://github.com/Kitware/CMake/releases/download/v3.14.0/cmake-3.14.0-Linux-x86_64.sh
RUN chmod +x cmake-3.14.0-Linux-x86_64.sh
RUN bash cmake-3.14.0-Linux-x86_64.sh --prefix=/usr/local --skip-license
RUN rm cmake-3.14.0-Linux-x86_64.sh

# Install Python dependencies
RUN pip3 install \
    pytest \
    Pillow \
    palettable

# Download public keys for github
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

# Clone openssl repo
WORKDIR /root
RUN --mount=type=ssh git clone -b 'OpenSSL_1_0_1g' --single-branch --depth 1 git@github.com:openssl/openssl.git openssl
ENV OPENSSL_DIR /root/openssl

# Install openssl
WORKDIR /root/openssl
ENV CC "python3 /root/fuzzview/fv-compiler.py"
RUN mkdir bin
RUN ./config no-threads --prefix=/root/openssl/bin --openssldir=/root/openssl/bin/openssl
RUN make
RUN make install_sw

# # Copy root folder
# WORKDIR /root
# RUN mkdir fuzzview
# COPY ./ /root/fuzzview/

# Set fuzzview location
ENV FV_DIR /root/fuzzview
