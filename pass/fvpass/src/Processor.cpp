#include "Processor.hpp"

using namespace fv;

Processor::Processor() {
    cfg_builder = CfgBuilder();
}

bool Processor::hasFuncDef(llvm::Module &M) {

    auto F_iter = M.begin();

    while (F_iter->isDeclaration() && F_iter != M.end()) F_iter++;

    return F_iter != M.end();
}

void Processor::processModule(llvm::Module &M) {

    // Check if there are only declarations
    // to prevent making cfg for "empty" file.
    if (!hasFuncDef(M)) return;

    cfg_builder.addModule(M);
    uint32_t func_counter = 0;

    for (auto &F : M) {

        if (F.isDeclaration()) continue;

        cfg_builder.addFunction(F, func_counter);
        uint32_t block_counter = 0;

        for (auto &B : F) {

            cfg_builder.addBlock(B, block_counter);

            block_counter++;
        }

        func_counter++;
    }

    cfg_builder.save();
}
