#ifndef FV_PROCESSOR_H
#define FV_PROCESSOR_H

#include "llvm/IR/Module.h"
#include "llvm/IR/DebugInfoMetadata.h"
#include "llvm/Support/Path.h"

#include <iostream>
#include <fstream>

#include "Cfg.hpp"

namespace fv {

class Processor {

  private:

    llvm::Instruction *getFirstInstruction(llvm::Module &M);
    std::string getFullFilePath(llvm::Module &M);
    void saveFile(llvm::Module &M);

  public:

    Processor();

    void processModule(llvm::Module &M);

};

}

#endif
