#ifndef FV_PROCESSOR_H
#define FV_PROCESSOR_H

#include <iostream>

#include "llvm/IR/Module.h"

#include "Cfg.hpp"

namespace fv {

class Processor {

  private:

    Cfg cfg_maker;

  public:

    Processor();

    void processModule(llvm::Module &M);

};

}

#endif
