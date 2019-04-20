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

#include "CfgBuilder.hpp"

using namespace fv;

void CfgTermInstVisitor::visitBranchInst(
    llvm::BranchInst &branch_inst) {

    if (branch_inst.isConditional()) {

        branch_json["type"] = "condition";
        branch_json["dest"] = json::object();

        auto *block_false = branch_inst.getSuccessor(CONDITION_FALSE);
        branch_json["dest"][GET_BLOCK_ID(block_false)] = false;

        auto *block_true = branch_inst.getSuccessor(CONDITION_TRUE);
        branch_json["dest"][GET_BLOCK_ID(block_true)] = true;

    } else {

        branch_json["type"] = "direct";
    }
}

void CfgTermInstVisitor::visitSwitchInst(
    llvm::SwitchInst &switch_inst) {

    branch_json["type"] = "switch";
    branch_json["dest"] = json::object();

    auto *block_default = switch_inst.getDefaultDest();
    branch_json["dest"][GET_BLOCK_ID(block_default)] = "default";

    for (auto switch_case : switch_inst.cases()) {

        auto *block_case = switch_case.getCaseSuccessor();
        branch_json["dest"][GET_BLOCK_ID(block_case)] = 
            switch_case.getCaseValue()->getSExtValue();
    }
}

// TODO: Have not encountered this yet.
void CfgTermInstVisitor::visitIndirectBrInst(
    llvm::IndirectBrInst &indir_br_inst) {

    Error::fatal<llvm::IndirectBrInst>(&indir_br_inst, 
        "Indirect branch instructions currently not supported");
}

// Other terminating instructions (e.g. return) are
// not relevant to us.
void CfgTermInstVisitor::visitTerminatorInst(
    llvm::TerminatorInst &term_inst) { }

void CfgTermInstVisitor::visitInstruction(
    llvm::Instruction &I) { }
