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

#ifndef ERROR_H
#define ERROR_H

#include <iostream>

#include "llvm/Support/raw_ostream.h"

// Helper to print errors nicely and consistently,
// and exit on fatal errors, indicating failure to
// calling script.
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
    static void fatal(const LLVM_TYPE *llvm_var, std::string msg) {
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
