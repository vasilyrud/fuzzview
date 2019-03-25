#ifndef FV_PROCESSOR_H
#define FV_PROCESSOR_H

#include <iostream>

#include "CfgBuilder.hpp"

#define WAS_PROCESSED_MD_NAME "fv.processed"

namespace fv {

class Processor {

  public:

    Processor();

    void processModule(llvm::Module &M);

  private:

    CfgBuilder cfg_builder;

    bool hasFuncDef(llvm::Module &M);
    void assignBlockIds(llvm::Function &F);

    bool wasProcessed(llvm::Module &M);
    void setProcessed(llvm::Module &M);

};

}

#endif
