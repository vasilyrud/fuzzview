import os
import sys
import json
import pytest
import subprocess

import fuzzview.const as const
import fuzzview.util as util

@pytest.fixture(scope="module")
def compile_prog_cfg():

    os.chdir(util.getenv(const.FV_ENV_VAR) + '/pass/fvpass/test/samples')

    compile_cmd = ''
    compile_cmd += util.getenv(const.LLVM_ENV_VAR) + '/bin/clang '
    compile_cmd += '-O0 -Wall -g '
    compile_cmd += '-Xclang -load -Xclang ' + util.getenv(const.FV_ENV_VAR) + '/pass/build/fvpass/libFvPass.so '
    compile_cmd += 'prog1.c -o bin/prog1 '

    new_env = os.environ.copy()

    new_env[const.NICE_JSON_ENV_VAR] = '1'

    proc_ret = subprocess.run(
        compile_cmd.split(' '),
        env=new_env
    )

    cfg_file = util.getenv(const.FV_ENV_VAR) + '/pass/fvpass/test/samples/prog1.cfg.json'

    with open(cfg_file) as f:
        cfg = json.load(f)
    
    return cfg

def test_module_name(compile_prog_cfg):
    cfg = compile_prog_cfg

    assert cfg['path'] == util.getenv(const.FV_ENV_VAR) + '/pass/fvpass/test/samples'
    assert cfg['name'] == 'prog1'
    assert cfg['extension'] == '.c'

def test_functions(compile_prog_cfg):
    cfg = compile_prog_cfg
    funcs = cfg['functions']

    assert 'A' in funcs
    assert 'B' in funcs
    assert 'C' in funcs
    assert 'D' in funcs

def test_calls(compile_prog_cfg):
    cfg = compile_prog_cfg
    funcs = cfg['functions']
    blocks = funcs['A']['blocks']

    block = blocks['0']
    assert blocks['0']['calls'] == []

    block = blocks['1']
    assert block['calls'][0]['type'] == 'indirect'
    assert block['calls'][0]['signature'] == 'i32 ()'

    block = blocks['2']
    assert block['calls'][0]['type'] == 'direct'
    assert block['calls'][0]['function'] == 'B'
    assert block['calls'][0]['signature'] == 'i32 ()'

    block = blocks['5']
    assert len(block['calls']) == 2

def test_prev_next(compile_prog_cfg):
    cfg = compile_prog_cfg
    funcs = cfg['functions']
    blocks = funcs['A']['blocks']

    block = blocks['0']
    assert block['prev'] == []
    assert block['next'] == ['1', '2']

    block = blocks['4']
    assert len(block['prev']) == 1
    assert len(block['next']) == 1

    block = blocks['6']
    assert len(block['prev']) == 2

def test_branches(compile_prog_cfg):
    cfg = compile_prog_cfg
    funcs = cfg['functions']
    blocks = funcs['A']['blocks']

    block = blocks['0']
    assert block['branch']['type'] == 'condition'
    assert block['branch']['dest']['1'] == True
    assert block['branch']['dest']['2'] == False
    
    block = blocks['1']
    assert block['branch']['type'] == 'direct'

    block = blocks['3']
    assert block['branch']['type'] == 'switch'
    assert block['branch']['dest']['4'] == 7
    assert block['branch']['dest']['5'] == 'default'
