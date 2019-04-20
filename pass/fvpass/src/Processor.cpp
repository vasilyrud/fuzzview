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

*/

#include "Processor.hpp"

using namespace fv;

Processor::Processor() {
    cfg_builder = CfgBuilder();
}

// Are there any functions with basic
// blocks in this module?
bool Processor::hasFuncDef(llvm::Module &M) {

    auto F_iter = M.begin();

    while (F_iter->isDeclaration() && F_iter != M.end()) F_iter++;

    return F_iter != M.end();
}

// Assign block IDs that are unique per module.
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

// Make a note globally in the IR metadata.
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

    // Make a note in the IR that the module
    // has been processed.
    setProcessed(M);
}
