#ifndef FV_PROCESSOR_H
#define FV_PROCESSOR_H

#include <iostream>

#include "CfgBuilder.hpp"

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
