# fuzzview

## Prerequisites

Works with LLVM version 7.0.1

Requires `dot` (graphviz)

## To get started

Set `FV_LLVM_DIR` to the location of LLVM install:

```
export FV_LLVM_DIR=/path/to/llvm/install
```

Set `FV_DIR` to the location of this folder:

```
export FV_DIR=/path/to/fuzzview
```

To compile LLVM pass:

```
cd $FV_DIR/pass
mkdir build
cd build
cmake ..
make
```

To compile test progs with custom clang:

```
cd $FV_DIR/tests/progs
make
```

To make `.cfg.json` files readable, set before compiling:

```
FV_NICE_JSON=1
```

Running fuzzview:

```
PYTHONPATH="${PYTHONPATH}:${FV_DIR}/fuzzview" python3 fuzzview $FV_DIR/tests/progs
```

Running tests:

```
PYTHONPATH="${PYTHONPATH}:${FV_DIR}/fuzzview" python3 -m pytest -x
```
