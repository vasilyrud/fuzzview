#ifndef FV_CFG_BUILDER_H
#define FV_CFG_BUILDER_H

#include <iostream>
#include <fstream>
#include <iomanip>

#include "llvm/IR/CFG.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/InstVisitor.h"
#include "llvm/Analysis/CFG.h"
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

    void save(llvm::Module &M);

  private:

    json file_json;

    void addBackEdges(llvm::Function &F, json &back_edges_json);
    void addCalls(llvm::BasicBlock &B, json &calls_json);
    void addCall(llvm::CallInst *call_inst, json &calls_json);
    bool ignoredFunc(std::string &func_name);
    std::string getFuncTypeStr(llvm::FunctionType *func_type);
    void addPrev(llvm::BasicBlock &B, json &prev_json);
    void addNext(llvm::BasicBlock &B, json &next_json);
    void addBranch(llvm::BasicBlock &B, json &branch_json);

    std::string getPath(llvm::Module &M);
    std::string getName(llvm::Module &M);
    std::string getExtension(llvm::Module &M);

    bool isExtensionDot(std::string raw_filename, size_t dot_location);
    std::string rmFileExtension(std::string raw_filename);
    std::string getFileExtension(std::string raw_filename);
    llvm::Instruction *getFirstInstruction(llvm::Module &M);

};

struct CfgTermInstVisitor : public llvm::InstVisitor<CfgTermInstVisitor, void> {

    using json = nlohmann::json;

    llvm::BasicBlock &B;
    json &branch_json;

    CfgTermInstVisitor(llvm::BasicBlock &B, json &branch_json) : 
    B(B), branch_json(branch_json) { }

    void visitBranchInst(llvm::BranchInst &branch_inst);
    void visitSwitchInst(llvm::SwitchInst &switch_inst);
    void visitIndirectBrInst(llvm::IndirectBrInst &indir_br_inst);

    void visitTerminatorInst(llvm::TerminatorInst &term_inst);
    void visitInstruction(llvm::Instruction &I);

};

}

#endif
