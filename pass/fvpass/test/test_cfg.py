import os
import sys
import json
import subprocess

FV_ENV_VAR = 'FUZZVIEW_DIR'
LLVM_ENV_VAR = 'LLVM_HOME'
NICE_JSON_ENV_VAR = 'FV_NICE_JSON'

def getenv(env_var):

    var_val = os.environ.get(env_var)

    if var_val is None:
        print(env_var + ' is not set.')
        sys.exit(1)
    
    return var_val

def compile_prog():

    os.chdir(getenv(FV_ENV_VAR) + '/pass/fvpass/test/samples')

    compile_cmd = ''
    compile_cmd += getenv(LLVM_ENV_VAR) + '/bin/clang '
    compile_cmd += '-O0 -Wall -g '
    compile_cmd += '-Xclang -load -Xclang ' + getenv(FV_ENV_VAR) + '/pass/build/fvpass/libFvPass.so '
    compile_cmd += 'prog1.c -o bin/prog1 '

    new_env = os.environ.copy()

    # new_env[NICE_JSON_ENV_VAR] = '1'

    proc_ret = subprocess.run(
        compile_cmd.split(' '),
        env=new_env
    )

def check_cfg():

    cfg_file = getenv(FV_ENV_VAR) + '/pass/fvpass/test/samples/prog1.cfg.json'

    with open(cfg_file) as f:
        cfg = json.load(f)
    
    assert cfg['path'] == getenv(FV_ENV_VAR) + '/pass/fvpass/test/samples'
    assert cfg['name'] == 'prog1'
    assert cfg['extension'] == '.c'

    funcs = cfg['functions']
    assert 'A' in funcs and 'B' in funcs and 'C' in funcs and 'D' in funcs

    blocks = funcs['A']['blocks']

    block = blocks['0']
    assert block['calls'] == []
    assert block['prev'] == []
    assert block['next'] == ['1', '2']
    assert block['branch']['type'] == 'condition'
    assert block['branch']['dest']['1'] == True
    assert block['branch']['dest']['2'] == False
    
    block = blocks['1']
    assert block['calls'][0]['type'] == 'indirect'
    assert block['calls'][0]['signature'] == 'i32 ()'
    assert block['branch']['type'] == 'direct'

    block = blocks['2']
    assert block['calls'][0]['type'] == 'direct'
    assert block['calls'][0]['function'] == 'B'
    assert block['calls'][0]['signature'] == 'i32 ()'

    block = blocks['3']
    assert block['branch']['type'] == 'switch'
    assert block['branch']['dest']['4'] == 7
    assert block['branch']['dest']['5'] == 'default'

    block = blocks['4']
    assert len(block['prev']) == 1
    assert len(block['next']) == 1

    block = blocks['5']
    assert len(block['calls']) == 2

    block = blocks['6']
    assert len(block['prev']) == 2

    print("SUCCESS")

def main():

    compile_prog()
    check_cfg()

if __name__ == "__main__":
    main()
