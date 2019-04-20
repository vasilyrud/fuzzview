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

include_directories(src lib)

FILE(GLOB cppSrcs src/*.cpp)

add_library(FvPass MODULE
    lib/nlohmann/json.hpp
    FvPass.cpp
    ${cppSrcs}
)

# Use C++11
target_compile_features(FvPass PRIVATE cxx_range_for cxx_auto_type)

set_target_properties(FvPass PROPERTIES
    COMPILE_FLAGS "-fno-rtti"
)

# Get proper shared-library behavior (where symbols are not necessarily
# resolved when the shared library is linked) on OS X.
if(APPLE)
    set_target_properties(FvPass PROPERTIES
        LINK_FLAGS "-undefined dynamic_lookup"
    )
endif(APPLE)
