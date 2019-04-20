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

#ifndef FV_METADATA_H
#define FV_METADATA_H

#include "llvm/IR/Module.h"
#include "llvm/IR/DebugInfoMetadata.h"

#define METADATA_BLOCK_ID "fv.block.id"

#define GET_MD_STR(MD) \
    llvm::cast<llvm::MDString>(MD->getOperand(0))->getString().str()

namespace fv {

// Helper to set and get metadata, since
// every metadata access involves several
// non-obvious calls to get to the value.
class Metadata {

  public:

    // Set metadata to an instruction, something like:
    //     item.metadata[metadata_key] = data
    static void set(
        llvm::Instruction *item, 
        const std::string &metadata_key, 
        const std::string &data
    ) {

        item->setMetadata(metadata_key,
            llvm::MDNode::get(item->getContext(),
                llvm::MDString::get(item->getContext(), data)));
    }

    // Get metadata of an instruction, something like:
    //     return item.metadata[metadata_key]
    static std::string get(
        const llvm::Instruction *item, 
        const std::string &metadata_key
    ) {

        auto *MD = item->getMetadata(metadata_key);
        if (!MD)
            Error::fatal<llvm::Instruction>(item, "No " + metadata_key + " found.");

        return GET_MD_STR(MD);
    }

};

}

#endif
