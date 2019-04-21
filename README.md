# [WIP] fuzzview

[![Build Status](https://travis-ci.org/vasilyrud/fuzzview.svg?branch=master)](https://travis-ci.org/vasilyrud/fuzzview)
[![codecov](https://codecov.io/gh/vasilyrud/fuzzview/branch/master/graph/badge.svg)](https://codecov.io/gh/vasilyrud/fuzzview)

Fuzzview is a work-in-progress tool for completely visualizing coverage gained from fuzzing large target programs at a glance.

## Sections

- [Motivation](#motivation)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)

## Motivation

Selecting seeds for fuzzing and optimizing fuzzers and other automated testing tools always involves looking at where in the program the tools get stuck and why. I like seeing coverage using icicle or grid graphs, but such graphs only show data at a file granularity. Within each file, coverage is limited to per-line highlights or per-function `dot` graphs. Because of this, debugging a fuzzing run is often tedious, without a bird's eye view of the entire program's CFG.

Showing the CFG and callgraph of the entire program is difficult with normal graph visualization tools. These tools (e.g. `dot` or force-based graphs) show all edges and nodes in the classical sense, by drawing lines for all edges in the graph. This works well for small, arbitrary graphs, but doesn't scale well to the callgraphs and control-flow graphs (CFGs) of large programs. `d3` and other graph tools that use automatic force-based layouts scale badly to thousands of nodes and edges, and generally don't stay true to how CFGs really look. `dot` is extremely useful for exploring a single file or function, but drawing the callgraph or putting all CFGs side-by-side for even basic C libraries is already too much. 

Because CFGs always follow a particular pattern, it is easy to represent them in a condensed manner without loosing information. Fuzzview aims to bridge the gap between per-file coverage visualizations and the grid view of the entire program, to provide instant feedback to the tester about how the fuzzing run is going.

That being said, this tool is at the early stage of testing how well the idea transfers into reality :grinning: .

## Installation

Using custom LLVM passes can be annoying, due to the tight coupling of the pass with a specific version of the LLVM C++ interface. It is recommended that you setup and use fuzzview inside a docker container.

### Setting up with Docker

To create the docker image, run the following command from inside the fuzzview directory:

```bash
docker build -t fuzzview -f Dockerfile .
```

Start using the docker container with:

```bash
export FV_DOCKER_CONTAINER=$(docker run -it -d fuzzview /bin/bash)
docker exec -it $FV_DOCKER_CONTAINER bash
```

### Setting up manually

You can install fuzzview on your own system manually.

#### Dependencies

You will need to satisfy the following dependencies:

- The fuzzview LLVM pass works best and is tested only with LLVM version 7.0.1.
- `cmake` of at least version 3.13 and `clang` 7.0.1 are used for building the LLVM pass. The default Mac OSX clang compiler is not supported.
- For now, `dot` (graphviz) is used to save `.dot` files besides all fuzzview image files for comparison.
- Python version >= 3.5 is required.

The easiest way to get LLVM 7.0.1 is to download the pre-built binaries for your system or to compile from source. You can get LLVM here: [LLVM 7.0.1](http://releases.llvm.org/download.html#7.0.1). It is likely that LLVM 7.0.0 will also work well, if 7.0.1 binaries for your system are not available.

#### Set environment variables

Set `FV_LLVM_DIR` to the location of the LLVM install. This will be used to automatically fetch the location of LLVM headers and the clang compiler.

```bash
export FV_LLVM_DIR=/path/to/llvm/install
```

Set `FV_DIR` to the location of this folder. This is mainly used by tests as well as to find the location of the LLVM pass.

```bash
export FV_DIR=/path/to/fuzzview
```

#### Compile LLVM pass

To compile the LLVM pass:

```bash
cd $FV_DIR/pass
mkdir build
cd build
cmake ..
make
```

#### Compile Python programs

Both the compiler wrapper and the fuzzview cli should work out of the box without any setup, but to install Python dependencies automatically, you can run:

```bash
cd $FV_DIR
pip3 install -e ./fuzzview
```

The above command is required to run tests as well.

## Usage

To run fuzzview on a program you first need to compile the program with the fuzzview LLVM pass. This step will allow fuzzview to save any necessary files in the program source directories, as well as to insert extra instrumentation.

The `fv-compiler.py` compiler wrapper that will help set all the compiler flags for you.

### Compiling with LLVM pass

Only C target programs are currently supported.

To compile any C program, set the C compiler to:

```bash
export CC="python3 $FV_DIR/fv-compiler.py"
```

Then run `configure`, `make`, or any other commands normally used to compile the target program.

To compile a single file with the LLVM pass, run `python3 $FV_DIR/fv-compiler.py myprog.c -o myprog` instead of `gcc myprog.c -o myprog`.

#### Extra options (env vars)

`FV_NICE_JSON=1`: makes the `.cfg.json` files which the LLVM pass outputs human-readable.

### Running fuzzview

After a program has been compiled with the LLVM pass, you can run fuzzview to generate fuzzview graph files. To do so, point fuzzview to the directory of the target program's source:

```bash
python3 $FV_DIR/fuzzview dir /path/to/target/source
```

At the moment, fuzzview does not do more than generate condensed graph images for each file. Check back later for updates on a more complete workflow!

## Testing

Mac OSX is not officially supported, but fuzzview should work if you install your own version of LLVM/clang.

After completing steps in the [Installation](#installation) section, run:

```bash
cd $FV_DIR
python3 -m pytest -x
```

To generate image files for the supplied test programs:

```bash
python3 $FV_DIR/fuzzview dir $FV_DIR/tests/progs
```

## Contributing

The project is in its early stages. Please check back later to see how you can contribute.
