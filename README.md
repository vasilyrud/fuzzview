# fuzzview

## Prerequisites

Works with LLVM version 7.0.1

Requires `dot` (graphviz)

## To get started

Set `LLVM_HOME` to the location of LLVM install:

```
export LLVM_HOME=/path/to/llvm/install
```

Set `FUZZVIEW_DIR` to the location of this folder:

```
export FUZZVIEW_DIR=/path/to/fuzzview
```

To compile LLVM pass:

```
cd $FUZZVIEW_DIR/pass
mkdir build
cd $FUZZVIEW_DIR/pass/build
CC=$LLVM_HOME/bin/clang CXX=$LLVM_HOME/bin/clang++ cmake ..
make
```

To compile test progs with custom clang:

```
cd $FUZZVIEW_DIR/tests/progs
make
```

To make `.cfg.json` files readable, set before compiling:

```
FV_NICE_JSON=1 
```

Running fuzzview:

```
PYTHONPATH="${PYTHONPATH}:${FUZZVIEW_DIR}/fuzzview" python3 fuzzview $FUZZVIEW_DIR/tests/progs
```

Running tests:

```
PYTHONPATH="${PYTHONPATH}:${FUZZVIEW_DIR}/fuzzview" python3 -m pytest -x
```
