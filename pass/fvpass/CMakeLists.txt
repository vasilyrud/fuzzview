# Source:
# https://github.com/abenkhadra/llvm-pass-tutorial
# commit 29481466d7c1b3e71c08f0013500534b3a8ed6c7

FILE(GLOB cppSrcs ./*.cpp)

add_library(FvPass MODULE
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
