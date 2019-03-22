#ifndef FV_METADATA_H
#define FV_METADATA_H

#include "llvm/IR/Module.h"
#include "llvm/IR/DebugInfoMetadata.h"

#define METADATA_BLOCK_ID "fv.block.id"

#define GET_MD_STR(MD) \
    llvm::cast<llvm::MDString>(MD->getOperand(0))->getString().str()

namespace fv {

class Metadata {

  public:

    static void set(
        llvm::Instruction *item, 
        const std::string &metadata_key, 
        const std::string &data
    ) {

        item->setMetadata(metadata_key,
            llvm::MDNode::get(item->getContext(),
                llvm::MDString::get(item->getContext(), data)));
    }

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
