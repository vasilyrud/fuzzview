#include "CfgBuilder.hpp"

using namespace fv;

CfgBuilder::CfgBuilder() {}

bool CfgBuilder::isExtensionDot(std::string raw_filename, size_t dot_location) {
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
std::string CfgBuilder::rmFileExtension(std::string raw_filename) {

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
std::string CfgBuilder::getFileExtension(std::string raw_filename) {

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

llvm::Instruction *CfgBuilder::getFirstInstruction(llvm::Module &M) {

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

std::string CfgBuilder::getFullFilePath(llvm::Module &M) {

    auto *I = getFirstInstruction(M);
    const llvm::DILocation *loc = I->getDebugLoc().get();

    return loc->getDirectory().str() + "/" + loc->getFilename().str();
}

std::string CfgBuilder::getRelativeFilePath(llvm::Module &M) {

    return M.getName().str();
}

void CfgBuilder::addModule(llvm::Module &M) {

    full_file_path = getFullFilePath(M);
    relative_file_path = getRelativeFilePath(M);

    file_json["file_path"] = rmFileExtension(full_file_path);
    file_json["source_extension"] = getFileExtension(full_file_path);
    file_json["functions"] = json::object();
}

void CfgBuilder::addFunction(llvm::Function &F, uint32_t func_number) {

    if (!file_json.count("functions"))
        Error::fatal("Did not call addModule yet.");

    std::string func_name = F.getName().str();

    json func_json = json::object();

    func_json["number"] = func_number;
    func_json["blocks"] = json::object();

    file_json["functions"][func_name] = func_json;
}

void CfgBuilder::addBlock(llvm::BasicBlock &B, uint32_t block_number) {

    if (!file_json.count("functions"))
        Error::fatal("Did not call addModule yet.");

    std::string block_name = std::to_string(block_number);
    std::string func_name  = B.getParent()->getName().str();

    if (!file_json["functions"].count(func_name))
        Error::fatal("Did not call addFunction on " + func_name + " yet.");

    json block_json = json::object();

    block_json["number"] = block_number;
    
    json calls_json = json::array();
    addCalls(B, calls_json);
    block_json["calls"] = calls_json;

    json prev_json = json::array();
    addPrev(B, prev_json);
    block_json["prev"] = prev_json;

    json next_json = json::array();
    addNext(B, next_json);
    block_json["next"] = next_json;

    json edges_json = json::array();
    addEdges(B, edges_json);
    block_json["edges"] = edges_json;

    file_json["functions"][func_name]["blocks"][block_name] = block_json;
}

void CfgBuilder::addCalls(llvm::BasicBlock &B, json &calls_json) {

    for (auto &I : B) {
        
        auto *call_inst = llvm::dyn_cast<llvm::CallInst>(&I);

        if (call_inst)
            addCall(call_inst, calls_json);;
    }
}

void CfgBuilder::addCall(llvm::CallInst *call_inst, json &calls_json) {

    json call_json = json::object();
    llvm::FunctionType *func_type;

    auto *value = call_inst->getCalledValue()->stripPointerCasts();
    auto *called_func = llvm::dyn_cast<llvm::Function>(value);

    if (called_func) {

        auto called_func_name = called_func->getName().str();

        if (ignoredFunc(called_func_name)) return;

        call_json["is_direct"] = true;
        call_json["function"]  = called_func_name;

        func_type = called_func->getFunctionType();

    } else {

        call_json["is_direct"] = false;

        func_type = call_inst->getFunctionType();
    }

    call_json["function_type"] = getFuncTypeStr(func_type);

    calls_json.push_back(call_json);
}

bool CfgBuilder::ignoredFunc(std::string &func_name) {

    return (
        func_name == "llvm.dbg.declare"
    );
}

std::string CfgBuilder::getFuncTypeStr(llvm::FunctionType *func_type) {

    std::string func_type_str;
    llvm::raw_string_ostream ostream(func_type_str);   

    func_type->print(ostream);
    ostream.flush();

    return func_type_str;
}

void CfgBuilder::addPrev(llvm::BasicBlock &B, json &prev_json) {

    for (
        llvm::pred_iterator iter = llvm::pred_begin(&B), end = llvm::pred_end(&B);
        iter != end;
        ++iter
    ) {
        prev_json.push_back(GET_BLOCK_ID(*iter));
    }
}

void CfgBuilder::addNext(llvm::BasicBlock &B, json &next_json) {

    for (
        llvm::succ_iterator iter = llvm::succ_begin(&B), end = llvm::succ_end(&B);
        iter != end;
        ++iter
    ) {
        next_json.push_back(GET_BLOCK_ID(*iter));
    }
}

void CfgBuilder::addEdges(llvm::BasicBlock &B, json &edges_json) {

    auto *term_inst = B.getTerminator();

    std::string block_id = Metadata::get(term_inst, METADATA_BLOCK_ID);
}

void CfgBuilder::save() {

    std::string cur_dir = ".";
    std::string full_path = cur_dir + "/" + rmFileExtension(relative_file_path) + ".cfg.json";

    std::ofstream f;
    f.open (full_path, std::ios::out | std::ios::trunc);

    if (f.is_open()) {
        
        if (getenv(NICE_JSON_ENV_VAR))
            f << std::setw(4) << file_json << "\n";
        else
            f << file_json << "\n";

        f.close();
    } else Error::fatal("Couldn't open file " + full_path);
}
