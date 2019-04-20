// Based on boilerplate from:
// https://github.com/abenkhadra/llvm-pass-tutorial
// commit 29481466d7c1b3e71c08f0013500534b3a8ed6c7

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
