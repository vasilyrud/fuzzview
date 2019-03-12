#ifndef ERROR_H
#define ERROR_H

#include <iostream>

class Error {

  private:

    static void exit_start() {
        std::cerr << '\n';
        std::cerr << "--------------------\n";
        std::cerr << "fuzzview pass ERROR:\n";
    }

    static void exit_msg(std::string msg) {
        std::cerr << msg << '\n';
    }

    static void exit_end() {
        std::cerr << "--------------------\n";
        std::cerr << '\n';

        exit(1);
    }

  public:

    template<typename LLVM_TYPE>
    static void fatal(LLVM_TYPE *llvm_var, std::string msg) {
        exit_start();
        exit_msg(msg);

        if (llvm_var != nullptr) {
            std::cerr << "LLVM variable dump:\n";
            llvm_var->dump();
        }
        
        exit_end();
    }

    static void fatal(std::string msg) {
        exit_start();
        exit_msg(msg);
        exit_end();
    }

};

#endif
