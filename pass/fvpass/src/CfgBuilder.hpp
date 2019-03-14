#ifndef FV_CFG_BUILDER_H
#define FV_CFG_BUILDER_H

#include <iostream>
#include <fstream>
#include <iomanip>

#include "llvm/IR/CFG.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/InstVisitor.h"
#include "llvm/Support/Path.h"

#include "nlohmann/json.hpp"

#include "Error.hpp"
#include "Metadata.hpp"

#define NICE_JSON_ENV_VAR "FV_NICE_JSON"

#define CONDITION_TRUE  0
#define CONDITION_FALSE 1

#define GET_BLOCK_ID(BLOCK_PTR) \
    Metadata::get((BLOCK_PTR)->getTerminator(), METADATA_BLOCK_ID)

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
    std::string getFuncTypeStr(llvm::FunctionType *func_type);
    void addPrev(llvm::BasicBlock &B, json &prev_json);
    void addNext(llvm::BasicBlock &B, json &next_json);
    void addBranch(llvm::BasicBlock &B, json &branch_json);

    llvm::Instruction *getFirstInstruction(llvm::Module &M);
    std::string getFullFilePath(llvm::Module &M);
    std::string getRelativeFilePath(llvm::Module &M);

    bool isExtensionDot(std::string raw_filename, size_t dot_location);
    std::string rmFileExtension(std::string raw_filename);
    std::string getFileExtension(std::string raw_filename);

};

struct CfgTermInstVisitor : public llvm::InstVisitor<CfgTermInstVisitor, void> {

    using json = nlohmann::json;

    llvm::BasicBlock &B;
    json &branch_json;

    CfgTermInstVisitor(llvm::BasicBlock &B, json &branch_json) : 
    B(B), branch_json(branch_json) { }

    void visitBranchInst(llvm::BranchInst &BI);
    void visitSwitchInst(llvm::SwitchInst &SI);
    void visitIndirectBrInst(llvm::IndirectBrInst &II);

    void visitTerminatorInst(llvm::TerminatorInst &TI);
    void visitInstruction(llvm::Instruction &I);

};

}

#endif
