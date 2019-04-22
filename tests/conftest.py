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
import json
import pytest
import subprocess

from fuzzview.cfg.grapher import DirGrapher
from fuzzview.cfg.dot.filegraph import DotFileGraph
from fuzzview.cfg.fv.filegraph import FVFileGraph
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

    dir_grapher = DirGrapher(util.getenv(const.FV_ENV_VAR) + '/' + PROGS_DIR)

    # generate dot graph pdfs
    dir_grapher.save_graphs(DotFileGraph)
    # generate fv graph images
    dir_grapher.save_graphs(FVFileGraph)

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
