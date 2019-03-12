# fuzzview

Works with LLVM version 7.0.1

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

To compile examples with custom clang:

```
cd $FUZZVIEW_DIR/examples
make CC=$LLVM_HOME/bin/clang
```
