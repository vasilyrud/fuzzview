#ifndef FV_PROCESSOR_H
#define FV_PROCESSOR_H

#include <iostream>

#include "llvm/IR/Module.h"

#include "CfgBuilder.hpp"

#define METADATA_BLOCK_ID "fv.block.id"

#define SET_METADATA(WHERE, KEY, DATA) \
    (WHERE)->setMetadata(KEY, \
            llvm::MDNode::get((WHERE)->getContext(), \
                llvm::MDString::get((WHERE)->getContext(), DATA)));

namespace fv {

class Processor {

  public:

    Processor();

    void processModule(llvm::Module &M);

  private:

    CfgBuilder cfg_builder;

    bool hasFuncDef(llvm::Module &M);

};

}

#endif
