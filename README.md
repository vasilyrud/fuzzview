# fuzzview

[![Build Status](https://travis-ci.org/vasilyrud/fuzzview.svg?branch=master)](https://travis-ci.org/vasilyrud/fuzzview)
[![codecov](https://codecov.io/gh/vasilyrud/fuzzview/branch/master/graph/badge.svg)](https://codecov.io/gh/vasilyrud/fuzzview)

## Sections

- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)

## Installation

Using custom LLVM passes can be annoying, due to the tight coupling of the pass with a specific version of the LLVM C++ interface. It is recommended that you setup and use fuzzview inside a docker container.

### Setting up with Docker

To create the docker image, run the following command from inside the fuzzview directory:

```
docker build -t fuzzview -f Dockerfile .
```

Start using the docker container with:

```
export FV_DOCKER_CONTAINER=$(docker run -it -d fuzzview /bin/bash)
docker exec -it $FV_DOCKER_CONTAINER bash
```

### Setting up manually

#### Prerequisites

To install fuzzview on your own system, you will need to satisfy the following dependencies:

- The fuzzview LLVM pass works best and is tested only with LLVM version 7.0.1.
- `cmake` of at least version 3.13 and `clang` 7.0.1 are used for building the LLVM pass. The default Mac OSX clang compiler is not supported.
- For now, `dot` (graphviz) is used to save `.dot` files besides all fuzzview image files for comparison.
- Python version >= 3.5 is required.

The easiest way to get LLVM 7.0.1 is to download the pre-built binaries for your system or to compile from source:

[LLVM 7.0.1](http://releases.llvm.org/download.html#7.0.1)

It is likely that LLVM 7.0.0 will also work well.

#### Set environment variables

Set `FV_LLVM_DIR` to the location of the LLVM install. This will be used to automatically fetch the location of LLVM headers and the clang compiler.

```
export FV_LLVM_DIR=/path/to/llvm/install
```

Set `FV_DIR` to the location of this folder. This is mainly used by tests as well as to find the location of the LLVM pass.

```
export FV_DIR=/path/to/fuzzview
```

#### Compile LLVM pass

To compile the LLVM pass:

```
cd $FV_DIR/pass
mkdir build
cd build
cmake ..
make
```

#### Compile Python programs

Both the compiler wrapper and the fuzzview cli should work out of the box without any setup, but to install Python dependencies automatically, you can run:

```
cd $FV_DIR
pip3 install -e ./fuzzview
```

The above command is required to run tests as well.

## Usage

To run fuzzview on a program you first need to compile the program with the fuzzview LLVM pass. This step will allow fuzzview to save any necessary files in the program source directories, as well as to insert extra instrumentation.

The `fv-compiler.py` compiler wrapper that will help set all the compiler flags for you.

### Compiling with LLVM pass

Only C target programs are currently supported.

To compile any C program, set:

```
export CC="python3 $FV_DIR/fv-compiler.py"
```

Then run `configure`, `make`, or any other commands normally used to compile the target program.

To compile a single file with the LLVM pass, run

```
python3 $FV_DIR/fv-compiler.py myprog.c -o myprog
```

instead of

```
gcc myprog.c -o myprog
```

To make the `.cfg.json` files which the LLVM pass outputs human-readable, set before compiling:

```
export FV_NICE_JSON=1
```

### Running fuzzview

After a program has been compiled with the LLVM pass, you can run fuzzview to generate fuzzview graph files. To do so, point fuzzview to the directory of the target program's source:

```
python3 $FV_DIR/fuzzview dir $FV_DIR/tests/progs
```

At the moment, fuzzview does not more than generate condensed graph images for each file. Check back later for updates on a more complete workflow!

## Testing

Mac OSX is not officially supported, but fuzzview should work if you install your own version of LLVM/clang.

After completing steps in the [Installation](#installation) section, run:

```
cd $FV_DIR
python3 -m pytest -x
```

## Contributing

The project is in its early stages. Please check back later to see how you can contribute.
