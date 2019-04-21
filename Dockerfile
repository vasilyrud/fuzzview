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

# Make the installation scripts dir
WORKDIR /root
RUN mkdir install

# Install LLVM
WORKDIR /root/install
COPY ./install/llvm.sh /root/install/llvm.sh
RUN bash /root/install/llvm.sh
ENV FV_LLVM_DIR /root/llvm/701/bin

# Install cmake (newer version than that available with apt)
WORKDIR /root/install
COPY ./install/cmake.sh /root/install/cmake.sh
RUN bash /root/install/cmake.sh /usr/local

# Make fuzzview folder
WORKDIR /root
RUN mkdir fuzzview
ENV FV_DIR /root/fuzzview
ARG fv_dir="/root/fuzzview"

# Install fuzzview LLVM pass
WORKDIR $fv_dir
RUN mkdir pass
COPY ./pass/ $fv_dir/pass/

WORKDIR /root/install
COPY ./install/pass.sh /root/install/pass.sh
RUN bash /root/install/pass.sh

# Install fuzzview Python program
WORKDIR $fv_dir
RUN mkdir fuzzview
COPY ./fuzzview/ $fv_dir/fuzzview/

WORKDIR $fv_dir
RUN pip3 install -e ./fuzzview

# Copy over tests
WORKDIR $fv_dir
RUN mkdir tests
COPY ./tests/ $fv_dir/tests/

# Copy fv-compiler
WORKDIR $fv_dir
COPY ./fv-compiler.py $fv_dir/fv-compiler.py

# Final entry location
WORKDIR $fv_dir
