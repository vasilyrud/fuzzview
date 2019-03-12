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

#include "Cfg.hpp"

using namespace llvm;

namespace {
struct FvPass : public ModulePass {
    
    static char ID;
    
    FvPass() : ModulePass(ID) {}

    virtual bool runOnModule(Module &M);

  private:

    fv::Cfg cfg;

};
}

char FvPass::ID = 0;

bool FvPass::runOnModule(Module &M) {

    errs() << M.getName() << "\n";

    cfg = fv::Cfg();

    return false;
}

static void registerFvPass(const PassManagerBuilder &, legacy::PassManagerBase &PM) {
    PM.add(new FvPass());
}

static RegisterStandardPasses RegisterFvPass(PassManagerBuilder::EP_OptimizerLast, registerFvPass);
static RegisterStandardPasses RegisterFvPass0(PassManagerBuilder::EP_EnabledOnOptLevel0, registerFvPass);
