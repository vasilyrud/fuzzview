#include "Cfg.hpp"

using namespace fv;

Cfg::Cfg() {}

bool Cfg::isExtensionDot(std::string raw_filename, size_t dot_location) {
    return (
        dot_location == std::string::npos || // e.g. "test"
        dot_location == 0                 || // e.g. ".test"
        raw_filename[dot_location-1] == '/'  // e.g. "/.test"
    );
}

/*
* Removes the last extension from the filename, e.g.:
* "test.c"   -> "test"
* "test.c.c" -> "test.c"
* ".test"    -> ".test"
*/
std::string Cfg::rmFileExtension(std::string raw_filename) {

    std::string new_filename = "";

    if (raw_filename.size() == 0)
        Error::fatal("Empty module filename.");

    size_t last_dot = raw_filename.find_last_of('.');
    if (isExtensionDot(raw_filename, last_dot))
        return raw_filename;

    // Copy old filename up until the last dot
    for (size_t i = 0; i < last_dot; i++)
        new_filename += raw_filename[i];

    return new_filename;
}

/*
* Gets the last extension from the filename, e.g.:
* "test.c"   -> ".c"
* "test.c.c" -> ".c"
* ".test"    -> ""
*/
std::string Cfg::getFileExtension(std::string raw_filename) {

    std::string extension = "";

    if (raw_filename.size() == 0)
        Error::fatal("Empty module filename.");

    size_t last_dot = raw_filename.find_last_of('.');
    if (isExtensionDot(raw_filename, last_dot))
        return extension;

    // Copy extension, including the dot
    for (size_t i = last_dot, end = raw_filename.size(); i < end; i++)
        extension += raw_filename[i];

    return extension;
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

void Cfg::addModule(llvm::Module &M) {

    full_file_path = getFullFilePath(M);
    relative_file_path = getRelativeFilePath(M);

    file_json["file_path"] = rmFileExtension(full_file_path);
    file_json["source_extension"] = getFileExtension(full_file_path);
    file_json["functions"] = json::object();
}

void Cfg::addFunction(llvm::Function &F, uint32_t func_number) {

    std::string func_name = F.getName().str();

    json func_json = json::object();

    func_json["func_number"] = func_number;
    func_json["blocks"] = json::object();

    file_json["functions"][func_name] = func_json;
}

void Cfg::addBlock(llvm::BasicBlock &B, uint32_t block_number) {

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
