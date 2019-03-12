#ifndef FV_PROCESSOR_H
#define FV_PROCESSOR_H

#include "llvm/IR/Module.h"

#include <iostream>

#include "Cfg.hpp"

namespace fv {

class Processor {

  public:

    Processor();

    void processModule(llvm::Module &M);

};

}

#endif
