#include "CfgBuilder.hpp"

using namespace fv;

void CfgTermInstVisitor::visitBranchInst(llvm::BranchInst &BI) {

    if (BI.isConditional()) {

        branch_json["type"] = "condition";
        branch_json["dest"] = json::object();

        auto *block_false = BI.getSuccessor(CONDITION_FALSE);
        branch_json["dest"][GET_BLOCK_ID(block_false)] = false;

        auto *block_true = BI.getSuccessor(CONDITION_TRUE);
        branch_json["dest"][GET_BLOCK_ID(block_true)] = true;

    } else {

        branch_json["type"] = "direct";
    }
}

void CfgTermInstVisitor::visitSwitchInst(llvm::SwitchInst &SI) {

    branch_json["type"] = "switch";

    return;
}

void CfgTermInstVisitor::visitIndirectBrInst(llvm::IndirectBrInst &indir_br_inst) {

    Error::fatal<llvm::IndirectBrInst>(&indir_br_inst, "Indirect branch instructions currently not supported");
    
    return;
}

void CfgTermInstVisitor::visitTerminatorInst(llvm::TerminatorInst &TI) {
    return;
}

void CfgTermInstVisitor::visitInstruction(llvm::Instruction &I) {
    return;
}
