# Copyright 2019 Vasily Rudchenko - Fuzzview
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

FV_ENV_VAR = 'FV_DIR'
LLVM_ENV_VAR = 'FV_LLVM_DIR'

NO_UNDEFS = ['-Wl,-z,defs', '-Wl,--no-undefined']
OPTIMIZATIONS = ['-O1', '-O2', '-O3', '-Os', '-Oz', '-O', '-Ofast', '-funroll-loops']

def getenv(env_var):
    var_val = os.environ.get(env_var)

    if var_val is None:
        print(env_var + ' is not set.')
        sys.exit(1)

    return var_val

def check_file(filename, extra_msg=None):
    if not os.path.isfile(filename):
        print(filename + ' not found.')
        if extra_msg:
            print(extra_msg)
        sys.exit(1)

def compiler_arg():
    compiler = getenv(LLVM_ENV_VAR) + '/bin/clang'
    check_file(compiler)

    return compiler

def fv_pass_args():
    fv_pass = getenv(FV_ENV_VAR) + '/pass/build/fvpass/libFvPass.so'
    check_file(fv_pass, extra_msg='Make sure to compile the LLVM pass first.')

    return ['-Xclang', '-load', '-Xclang', fv_pass]

def extra_args():
    return ['-g', '-O0', '-Wno-nullability-completeness', '-Wno-unused-variable']

def main(argv):
    # Set our own compiler
    new_args = [compiler_arg()]

    # Add our own args.
    new_args += fv_pass_args()
    new_args += extra_args()

    # Add relevant old args.
    for arg in argv:

        # To prevent disallowing undefined symbols 
        # in object files.
        if arg in NO_UNDEFS:
            continue

        # Ignore optimizations.
        if arg in OPTIMIZATIONS:
            continue

        new_args.append(arg)

    os.execvp(new_args[0], new_args)

if __name__ == "__main__":
    main(sys.argv[1:])
