import os
import sys
import json
import pytest
import subprocess

import fuzzview.const as const
import fuzzview.util as util

def test_compile(compile_progs):
    assert compile_progs[0].returncode == 0

def test_module_names(compile_progs, subA_common_cfg, subB_common_cfg):
    cfgA = subA_common_cfg
    cfgB = subB_common_cfg
    progs_dir = compile_progs[1]

    assert cfgA['path'] == util.getenv(const.FV_ENV_VAR) + '/' + progs_dir
    assert cfgA['name'] == 'subA/common'
    assert cfgA['extension'] == '.c'

    assert cfgB['path'] == util.getenv(const.FV_ENV_VAR) + '/' + progs_dir
    assert cfgB['name'] == 'subB/common'
    assert cfgB['extension'] == '.c'

def test_functions(compile_progs, branches1_cfg):
    cfg = branches1_cfg
    funcs = cfg['functions']

    assert 'A' in funcs
    assert 'B' in funcs
    assert 'C' in funcs
    assert 'D' in funcs

def test_direct_calls(compile_progs, branches1_cfg):
    cfg = branches1_cfg
    blocks = cfg['functions']['A']['blocks']

    block = blocks['0']
    assert blocks['0']['calls'] == []

    block = blocks['2']
    assert block['calls'][0]['type'] == 'direct'
    assert block['calls'][0]['function'] == 'B'
    assert block['calls'][0]['signature'] == 'i32 ()'

def test_indirect_calls(compile_progs, branches1_cfg):
    cfg = branches1_cfg
    blocks = cfg['functions']['A']['blocks']

    block = blocks['1']
    assert block['calls'][0]['type'] == 'indirect'
    assert block['calls'][0]['signature'] == 'i32 ()'

def test_multiple_calls(compile_progs, branches1_cfg):
    cfg = branches1_cfg
    blocks = cfg['functions']['A']['blocks']

    block = blocks['5']
    assert len(block['calls']) == 2

def test_prev_next(compile_progs, branches1_cfg):
    cfg = branches1_cfg
    blocks = cfg['functions']['A']['blocks']

    block = blocks['0']
    assert block['prev'] == []
    assert block['next'] == ['1', '2']

    block = blocks['4']
    assert len(block['prev']) == 1
    assert len(block['next']) == 1

    block = blocks['6']
    assert len(block['prev']) == 2

def test_conditional_branches(compile_progs, branches1_cfg):
    cfg = branches1_cfg
    blocks = cfg['functions']['A']['blocks']

    block = blocks['0']
    assert block['branch']['type'] == 'condition'
    assert block['branch']['dest']['1'] == True
    assert block['branch']['dest']['2'] == False

def test_direct_branches(compile_progs, branches1_cfg):
    cfg = branches1_cfg
    blocks = cfg['functions']['A']['blocks']

    block = blocks['1']
    assert block['branch']['type'] == 'direct'

def test_switch_branches(compile_progs, branches1_cfg):
    cfg = branches1_cfg
    blocks = cfg['functions']['A']['blocks']

    block = blocks['3']
    assert block['branch']['type'] == 'switch'
    assert block['branch']['dest']['4'] == 7
    assert block['branch']['dest']['5'] == 'default'

def test_back_edges_nested(compile_progs, loops1_cfg):
    cfg = loops1_cfg
    back_edges = cfg['functions']['main']['back_edges']

    assert ('4', '2') in back_edges.items()
    assert ('7', '1') in back_edges.items()

def test_back_edges_same_dest(compile_progs, loops1_cfg):
    cfg = loops1_cfg
    back_edges = cfg['functions']['main']['back_edges']

    assert ('11', '9') in back_edges.items()
    assert ('13', '9') in back_edges.items()

def test_back_edges_irreducible(compile_progs, loops1_cfg):
    cfg = loops1_cfg
    back_edges = cfg['functions']['main']['back_edges']

    assert ('23', '18') in back_edges.items()
    assert ('18', '19') not in back_edges.items()
    assert ('19', '22') not in back_edges.items()
    assert ('22', '23') not in back_edges.items()
