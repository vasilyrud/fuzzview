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
#include "llvm/Support/FileSystem.h"
#include "llvm/Support/MD5.h"

#include "nlohmann/json.hpp"

#include "Error.hpp"
#include "Metadata.hpp"

#define NICE_JSON_ENV_VAR "FV_NICE_JSON"

#define CFG_JSON_EXTENSION ".cfg.json"

#define CONDITION_TRUE  0
#define CONDITION_FALSE 1

#define GET_BLOCK_ID(BLOCK_PTR) \
    Metadata::get((BLOCK_PTR)->getTerminator(), METADATA_BLOCK_ID)

namespace fv {

// Used to create the json structure that stores
// a module's CFG.
//
// Must first add the module, then a function, and
// then all the function's blocks.
class CfgBuilder {

    using json = nlohmann::json;

  public:

    CfgBuilder();

    // Add module-specific details and init
    // the "functions" sub-object.
    void addModule(llvm::Module &M);

    // Add function-specific details and init
    // the "blocks" sub-object.
    //
    // func_number specifies the order of the
    // function in the IR of the module.
    void addFunction(llvm::Function &F, uint32_t func_number);

    // Add block-specific details.
    // 
    // block_number specifies the order of the
    // block in the IR of the function.
    void addBlock(llvm::BasicBlock &B, uint32_t block_number);

    // Save the json file to the same dir as
    // the source file, and using the same
    // base name.
    void save(llvm::Module &M);

  private:

    // Root json object used as base in addModule().
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

// Visit terminating instructions in order to
// generate CFG edges in the json structure.
struct CfgTermInstVisitor : public llvm::InstVisitor<CfgTermInstVisitor, void> {

    using json = nlohmann::json;

    llvm::BasicBlock &B;
    json &branch_json;

    // Once visitor is used per basic block
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
