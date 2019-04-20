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
