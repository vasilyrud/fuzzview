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

#ifndef FV_PROCESSOR_H
#define FV_PROCESSOR_H

#include <iostream>

#include "CfgBuilder.hpp"

#define WAS_PROCESSED_MD_NAME "fv.processed"

namespace fv {

// The processor loops through all the
// functions in the module and calls
// relevant methods of all the pass
// features.
class Processor {

  public:

    Processor();

    // To be called once to process the module.
    void processModule(llvm::Module &M);

  private:

    CfgBuilder cfg_builder;

    bool hasFuncDef(llvm::Module &M);
    void assignBlockIds(llvm::Function &F);

    bool wasProcessed(llvm::Module &M);
    void setProcessed(llvm::Module &M);

};

}

#endif
