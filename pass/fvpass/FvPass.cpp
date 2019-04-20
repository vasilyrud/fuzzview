/*

    Copyright 2019 Vasily Rudchenko - Fuzzview
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
   
        http://www.apache.org/licenses/LICENSE-2.0
   
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    This file is based on boilerplate code from:
    https://github.com/abenkhadra/llvm-pass-tutorial

*/

#include "llvm/Pass.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"

#include "nlohmann/json.hpp"

#include "Processor.hpp"

using namespace llvm;

namespace {
struct FvPass : public ModulePass {
    
    static char ID;
    
    FvPass() : ModulePass(ID) {}

    virtual bool runOnModule(Module &M);

  private:

    fv::Processor processor;

};
}

char FvPass::ID = 0;

bool FvPass::runOnModule(Module &M) {

    // The processor handles all the
    // details of the pass.
    processor = fv::Processor();
    processor.processModule(M);

    return false;
}

static void registerFvPass(const PassManagerBuilder &, legacy::PassManagerBase &PM) {
    PM.add(new FvPass());
}

// Make sure that the pass runs last.
static RegisterStandardPasses RegisterFvPass(PassManagerBuilder::EP_OptimizerLast, registerFvPass);
// Make sure that the pass is always enabled.
static RegisterStandardPasses RegisterFvPass0(PassManagerBuilder::EP_EnabledOnOptLevel0, registerFvPass);
