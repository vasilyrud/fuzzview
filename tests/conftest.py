import os
import sys
import json
import pytest
import subprocess

from fuzzview.cfg.grapher import DirGrapher
from fuzzview.cfg.dot.filegraph import DotFileGraph
import fuzzview.const as const
import fuzzview.util as util

PROGS_DIR = 'tests/progs'

@pytest.fixture(scope='session')
def compile_progs():
    os.chdir(util.getenv(const.FV_ENV_VAR) + '/' + PROGS_DIR)

    # make clean
    subprocess.run(['make', 'clean'])

    # make
    new_env = os.environ.copy()
    new_env[const.NICE_JSON_ENV_VAR] = '1'
    proc_ret = subprocess.run(
        ['make'],
        env=new_env
    )

    # generate dot graph pdfs
    dir_grapher = DirGrapher(util.getenv(const.FV_ENV_VAR) + '/' + PROGS_DIR)
    dir_grapher.save_graphs(DotFileGraph)

    return proc_ret, PROGS_DIR

def get_cfg(prog_name):
    cfg_file = util.getenv(const.FV_ENV_VAR) + '/' + PROGS_DIR + '/' + prog_name + const.CFG_JSON_EXTENSION

    with open(cfg_file) as f:
        cfg = json.load(f)
    
    return cfg, cfg_file

@pytest.fixture(scope='session')
def branches1_cfg():
    return get_cfg('branches1')

@pytest.fixture(scope='session')
def loops1_cfg():
    return get_cfg('loops1')

@pytest.fixture(scope='session')
def subA_common_cfg():
    return get_cfg('subA/common')

@pytest.fixture(scope='session')
def subB_common_cfg():
    return get_cfg('subB/common')
