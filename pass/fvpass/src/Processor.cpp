#include "Processor.hpp"

using namespace fv;

Processor::Processor() {
    cfg_maker = Cfg();
}

void Processor::processModule(llvm::Module &M) {

    // Check if there are only declarations
    // to prevent making cfg for "empty" file.

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
