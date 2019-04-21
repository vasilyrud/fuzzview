# fuzzview

[![Build Status](https://travis-ci.org/vasilyrud/fuzzview.svg?branch=master)](https://travis-ci.org/vasilyrud/fuzzview)

## Getting started

### Prerequisites

LLVM pass works best and is tested with LLVM version 7.0.1

### Set environment variables

Set `FV_LLVM_DIR` to the location of LLVM install:

```
export FV_LLVM_DIR=/path/to/llvm/install
```

Set `FV_DIR` to the location of this folder:

```
export FV_DIR=/path/to/fuzzview
```

### Compile LLVM pass

To compile LLVM pass:

```
cd $FV_DIR/pass
mkdir build
cd build
cmake ..
make
```

### Using LLVM pass

To compile any program with custom clang, set:

```
export CC="python3 $FV_DIR/fv-compiler.py"
```

To make `.cfg.json` files readable, set before compiling:

```
FV_NICE_JSON=1
```

### Running fuzzview

Running fuzzview on test progs:

```
cd $FV_DIR/tests/progs
make
cd $FV_DIR
python3 fuzzview dir $FV_DIR/tests/progs
```

Running tests:

```
cd $FV_DIR
pip3 install -e fuzzview
python3 -m pytest -x
```
