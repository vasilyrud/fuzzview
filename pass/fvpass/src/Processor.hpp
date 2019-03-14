#ifndef FV_PROCESSOR_H
#define FV_PROCESSOR_H

#include <iostream>

#include "llvm/IR/Module.h"

#include "Cfg.hpp"

namespace fv {

class Processor {

  public:

    Processor();

    void processModule(llvm::Module &M);

  private:

    Cfg cfg_maker;

    bool hasFuncDef(llvm::Module &M);

};

}

#endif
