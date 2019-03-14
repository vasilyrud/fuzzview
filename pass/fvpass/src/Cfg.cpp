#include "Cfg.hpp"

using namespace fv;

Cfg::Cfg() {}

/*
* Removes the last extension from the filename, e.g.:
* test.c   -> test
* test.c.c -> test.c
* .test    -> .test
*/
std::string Cfg::rmFileExtension(std::string raw_filename) {

    std::string new_filename = "";

    if (raw_filename.size() == 0)
        Error::fatal("Invalid module filename: " + raw_filename);

    int last_dot = -1;
    for (int i = 0, end = raw_filename.size(); i < end; i++)
        if (raw_filename[i] == '.')
            last_dot = i;

    if (last_dot == -1 || // e.g. "test"
        last_dot == 0  || // e.g. ".test"
        raw_filename[last_dot-1] == '/' // e.g. "/.test"
    ) return raw_filename;

    // Copy old filename up until the last dot
    for (int i = 0; i < last_dot; i++)
        new_filename += raw_filename[i];

    return new_filename;
}

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

std::string Cfg::getRelativeFilePath(llvm::Module &M) {

    return M.getName().str();
}

void Cfg::add_module(llvm::Module &M) {

    full_file_path = getFullFilePath(M);
    relative_file_path = getRelativeFilePath(M);

    file_json["file_path"] = full_file_path;
    file_json["functions"] = json::object();
}

void Cfg::add_function(llvm::Function &F) {

    // Create json object for function
}

void Cfg::add_block(llvm::BasicBlock &B) {

    // Add block in its function
}

void Cfg::save() {

    std::string cur_dir = ".";
    std::string full_path = cur_dir + "/" + rmFileExtension(relative_file_path) + ".cfg.json";

    std::ofstream f;
    f.open (full_path, std::ios::out | std::ios::trunc);

    if (f.is_open()) {
        
        f << file_json << "\n";

        f.close();
    } else Error::fatal("Couldn't open file " + full_path);
}
