#ifndef FV_CFG_H
#define FV_CFG_H

#include <iostream>
#include <fstream>

#include "llvm/IR/Module.h"
#include "llvm/IR/DebugInfoMetadata.h"
#include "llvm/Support/Path.h"

#include "Error.hpp"

namespace fv {

class Cfg {

  public:

    Cfg();

    void add_module(llvm::Module &M);
    void add_function(llvm::Function &F);
    void add_block(llvm::BasicBlock &B);

    void save();

  private:

    std::string full_file_path;
    std::string module_name;

    llvm::Instruction *getFirstInstruction(llvm::Module &M);
    std::string getFullFilePath(llvm::Module &M);
    std::string getModuleName(llvm::Module &M);

};

}

#endif
