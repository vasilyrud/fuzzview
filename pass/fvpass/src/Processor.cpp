#include "Processor.hpp"

using namespace fv;

Processor::Processor() {}


llvm::Instruction *Processor::getFirstInstruction(llvm::Module &M) {

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

void Processor::saveFile(llvm::Module &M) {

    /*
    * So far, seems to be a reliable way to
    * save a file into same dir as the source
    * file with LLVM.
    */
    std::string c_file_path = ".";

    std::string full_path = c_file_path + "/" + M.getName().str() + ".cfg.json";

    std::ofstream f;
    f.open (full_path, std::ios::out | std::ios::trunc);

    if (f.is_open()) {
        f << "Test\n";
        f.close();
    } else Error::fatal("Couldn't open file " + full_path);
}

std::string Processor::getFullFilePath(llvm::Module &M) {

    auto *I = getFirstInstruction(M);
    const llvm::DILocation *loc = I->getDebugLoc().get();

    return loc->getDirectory().str() + "/" + loc->getFilename().str();
}

void Processor::processModule(llvm::Module &M) {
    
    uint32_t block_counter;

    std::cout << getFullFilePath(M) << "\n";

    saveFile(M);

    for (auto &F : M) {

        if (F.isDeclaration()) continue;

        std::cout << F.getName().str() << "\n";

        // for (auto &B : F) {

        // }
    }
}
