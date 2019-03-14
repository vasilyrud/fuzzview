#ifndef FV_CFG_BUILDER_H
#define FV_CFG_BUILDER_H

#include <iostream>
#include <fstream>
#include <iomanip>

#include "llvm/IR/Module.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/DebugInfoMetadata.h"
#include "llvm/Support/Path.h"

#include "nlohmann/json.hpp"

#include "Error.hpp"

#define NICE_JSON_ENV_VAR "FV_NICE_JSON"

namespace fv {

class CfgBuilder {

    using json = nlohmann::json;

  public:

    CfgBuilder();

    void addModule(llvm::Module &M);
    void addFunction(llvm::Function &F, uint32_t func_number);
    void addBlock(llvm::BasicBlock &B, uint32_t block_number);

    void save();

  private:

    json file_json;

    std::string full_file_path;
    std::string relative_file_path;

    void addCalls(llvm::BasicBlock &B, json &calls_json);
    void addCall(llvm::CallInst *call_inst, json &calls_json);
    bool ignoredFunc(std::string &func_name);

    llvm::Instruction *getFirstInstruction(llvm::Module &M);
    std::string getFullFilePath(llvm::Module &M);
    std::string getRelativeFilePath(llvm::Module &M);

    bool isExtensionDot(std::string raw_filename, size_t dot_location);
    std::string rmFileExtension(std::string raw_filename);
    std::string getFileExtension(std::string raw_filename);

};

}

#endif
