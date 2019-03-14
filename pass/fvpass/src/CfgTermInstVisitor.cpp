#include "CfgBuilder.hpp"

using namespace fv;

void CfgTermInstVisitor::visitBranchInst(llvm::BranchInst &branch_inst) {

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

void CfgTermInstVisitor::visitSwitchInst(llvm::SwitchInst &switch_inst) {

    branch_json["type"] = "switch";
    branch_json["dest"] = json::object();

    auto *block_default = switch_inst.getDefaultDest();
    branch_json["dest"][GET_BLOCK_ID(block_default)] = "default";

    for (auto switch_case : switch_inst.cases()) {

        auto *block_case = switch_case.getCaseSuccessor();
        branch_json["dest"][GET_BLOCK_ID(block_case)] = switch_case.getCaseValue()->getSExtValue();
    }
}

void CfgTermInstVisitor::visitIndirectBrInst(llvm::IndirectBrInst &indir_br_inst) {

    Error::fatal<llvm::IndirectBrInst>(&indir_br_inst, "Indirect branch instructions currently not supported");
}

void CfgTermInstVisitor::visitTerminatorInst(llvm::TerminatorInst &term_inst) { }

void CfgTermInstVisitor::visitInstruction(llvm::Instruction &I) { }
