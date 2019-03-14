#include "Processor.hpp"

using namespace fv;

Processor::Processor() {
    cfg_maker = Cfg();
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

    uint32_t block_counter;

    cfg_maker.add_module(M);

    for (auto &F : M) {

        if (F.isDeclaration()) continue;

        cfg_maker.add_function(F);

        std::cout << F.getName().str() << "\n";

        for (auto &B : F) {

            cfg_maker.add_block(B);
        }
    }

    cfg_maker.save();
}
