# fuzzview

Set `LLVM_HOME` to the location of LLVM install:

```
export LLVM_HOME=/path/to/llvm/install
```

To compile LLVM pass:

```
cd pass
mkdir build
cd build
cmake ..
make
```

To compile examples with custom clang:

```
cd examples
make CC=$LLVM_HOME/bin/clang
```
