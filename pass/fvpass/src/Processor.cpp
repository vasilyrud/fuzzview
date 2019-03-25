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

void Processor::assignBlockIds(llvm::Function &F) {

    uint32_t block_counter = 0;
    for (auto &B : F) {

        Metadata::set(
            B.getTerminator(), 
            METADATA_BLOCK_ID, 
            std::to_string(block_counter)
        );

        block_counter++;
    }
}

bool Processor::wasProcessed(llvm::Module &M) {

    return M.getNamedMetadata(WAS_PROCESSED_MD_NAME) != nullptr;
}

void Processor::setProcessed(llvm::Module &M) {

    M.getOrInsertNamedMetadata(WAS_PROCESSED_MD_NAME);
}

void Processor::processModule(llvm::Module &M) {

    uint32_t func_counter;
    uint32_t block_counter;

    // Check if there are only declarations
    // to prevent processing an "empty" file.
    if (!hasFuncDef(M)) return;

    // Check if the module was already processed
    // by our pass. Can happen, for example, if
    // compiled .c -> .bc and then .bc -> .exe
    if (wasProcessed(M)) return;

    cfg_builder.addModule(M);

    func_counter = 0;
    for (auto &F : M) {

        // Don't care about declarations because
        // they don't have basic blocks.
        if (F.isDeclaration()) continue;

        // First, assign our own "ids" to basic blocks.
        assignBlockIds(F);

        // Then, actually process them.
        cfg_builder.addFunction(F, func_counter);

        block_counter = 0;
        for (auto &B : F) {

            cfg_builder.addBlock(B, block_counter);

            block_counter++;
        }

        func_counter++;
    }

    cfg_builder.save(M);

    setProcessed(M);
}
