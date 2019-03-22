import os
import sys
import pytest

from fuzzview.cfg.fvfilegraph import FVFileGraph

def test_depths(compile_progs, loops1_cfg):
    cfg = loops1_cfg
    graph = FVFileGraph(cfg)

    assert graph.module == cfg
