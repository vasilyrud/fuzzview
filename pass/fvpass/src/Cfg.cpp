#include "Cfg.hpp"

using namespace fv;

Cfg::Cfg() {}

llvm::Instruction *Cfg::getFirstInstruction(llvm::Module &M) {

    auto F_iter = M.begin();
    while (F_iter->isDeclaration() && F_iter != M.end()) F_iter++;

    if (F_iter == M.end())
        Error::fatal("no function");

    auto *F = &*F_iter;

    auto B_iter = F->begin();
    if (B_iter == F->end())
        Error::fatal("no basic block");

    auto B = &*B_iter;

    auto I_iter = B->begin();
    if (I_iter == B->end())
        Error::fatal("no instruction");

    return &*I_iter;
}

std::string Cfg::getFullFilePath(llvm::Module &M) {

    auto *I = getFirstInstruction(M);
    const llvm::DILocation *loc = I->getDebugLoc().get();

    return loc->getDirectory().str() + "/" + loc->getFilename().str();
}

std::string Cfg::getModuleName(llvm::Module &M) {

    return M.getName().str();
}

void Cfg::add_module(llvm::Module &M) {

    full_file_path = getFullFilePath(M);
    module_name = getModuleName(M);
}

void Cfg::add_function(llvm::Function &F) {

    // Create json object for function
}

void Cfg::add_block(llvm::BasicBlock &B) {

    // Add block in its function
}

void Cfg::save() {

    /*
    * So far, seems to be a reliable way to
    * save a file into same dir as the source
    * file with LLVM.
    */
    std::string c_file_path = ".";

    std::string full_path = c_file_path + "/" + module_name + ".cfg.json";

    std::ofstream f;
    f.open (full_path, std::ios::out | std::ios::trunc);

    if (f.is_open()) {
        f << "Test\n";
        f.close();
    } else Error::fatal("Couldn't open file " + full_path);
}
