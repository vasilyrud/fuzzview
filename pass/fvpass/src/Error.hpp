#ifndef ERROR_H
#define ERROR_H

#include <iostream>

class Error {

  private:

    static void exitStart() {
        std::cerr << '\n';
        std::cerr << "--------------------\n";
        std::cerr << "fuzzview pass ERROR:\n";
    }

    static void exitMsg(std::string msg) {
        std::cerr << msg << '\n';
    }

    static void exitEnd() {
        std::cerr << "--------------------\n";
        std::cerr << '\n';

        exit(1);
    }

  public:

    template<typename LLVM_TYPE>
    static void fatal(LLVM_TYPE *llvm_var, std::string msg) {
        exitStart();
        exitMsg(msg);

        if (llvm_var != nullptr) {
            std::cerr << "LLVM variable dump:\n";
            llvm_var->dump();
        }
        
        exitEnd();
    }

    static void fatal(std::string msg) {
        exitStart();
        exitMsg(msg);
        exitEnd();
    }

};

#endif
