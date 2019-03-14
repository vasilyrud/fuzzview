#ifndef FV_CFG_H
#define FV_CFG_H

#include <iostream>
#include <fstream>

#include "llvm/IR/Module.h"
#include "llvm/IR/DebugInfoMetadata.h"
#include "llvm/Support/Path.h"

#include "nlohmann/json.hpp"

#include "Error.hpp"

namespace fv {

class Cfg {

    using json = nlohmann::json;

  public:

    Cfg();

    void add_module(llvm::Module &M);
    void add_function(llvm::Function &F);
    void add_block(llvm::BasicBlock &B);

    void save();

  private:

    json file_json;

    std::string full_file_path;
    std::string relative_file_path;

    llvm::Instruction *getFirstInstruction(llvm::Module &M);
    std::string getFullFilePath(llvm::Module &M);
    std::string getRelativeFilePath(llvm::Module &M);
    std::string rmFileExtension(std::string raw_filename);

};

}

#endif
