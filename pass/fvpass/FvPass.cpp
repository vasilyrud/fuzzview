// Based on boilerplate from:
// https://github.com/abenkhadra/llvm-pass-tutorial
// commit 29481466d7c1b3e71c08f0013500534b3a8ed6c7

#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"

using namespace llvm;

namespace {
    struct FvPass : public FunctionPass {
        static char ID;
        FvPass() : FunctionPass(ID) {}

        virtual bool runOnFunction(Function &F) {
            errs() << F.getName() << "\n";
            return false;
        }
    };
}

char FvPass::ID = 0;

static void registerFvPass(const PassManagerBuilder &, legacy::PassManagerBase &PM) {
    PM.add(new FvPass());
}

static RegisterStandardPasses RegisterMyPass(PassManagerBuilder::EP_EarlyAsPossible, registerFvPass);
