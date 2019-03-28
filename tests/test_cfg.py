import os
import sys
import pytest

from fuzzview.cfg.fv.filegraph import FVFileGraph

def test_depths(compile_progs, loops1_cfg):
    cfg, cfg_file = loops1_cfg
    graph = FVFileGraph(cfg, cfg_file)

    node = graph.get_func_graph('main').nodes['0']
    assert node.shortest_depth == 0
    assert node.longest_depth  == 0

    node = graph.get_func_graph('main').nodes['1']
    assert node.shortest_depth == 1
    assert node.longest_depth  == 1

    node = graph.get_func_graph('main').nodes['4']
    assert node.shortest_depth == 3
    assert node.longest_depth  == 3

    node = graph.get_func_graph('main').nodes['9']
    assert node.shortest_depth == 7
    assert node.longest_depth  == 7

    node = graph.get_func_graph('main').nodes['16']
    assert node.shortest_depth == 8
    assert node.longest_depth  == 12

    node = graph.get_func_graph('main').nodes['18']
    assert node.shortest_depth == 10
    assert node.longest_depth  == 14

    node = graph.get_func_graph('main').nodes['22']
    assert node.shortest_depth == 10
    assert node.longest_depth  == 16

    node = graph.get_func_graph('main').nodes['25']
    assert node.shortest_depth == 12
    assert node.longest_depth  == 18

def test_dimensions(compile_progs, branches1_cfg):
    cfg, cfg_file = branches1_cfg
    graph = FVFileGraph(cfg, cfg_file)

    assert graph.get_func_graph('D').nodes['0'].only_node_dimensions == (1, 1)
    assert graph.get_func_graph('D').nodes['0'].dimensions == (1, 1)

    assert graph.get_func_graph('A').nodes['1'].only_node_dimensions == (1, 1)
    assert graph.get_func_graph('A').nodes['1'].dimensions == (2, 3)

    assert graph.get_func_graph('A').nodes['3'].only_node_dimensions == (2, 1)
    assert graph.get_func_graph('A').nodes['3'].dimensions == (2, 3)

    assert graph.get_func_graph('A').nodes['5'].only_node_dimensions == (1, 2)
    assert graph.get_func_graph('A').nodes['5'].dimensions == (2, 4)
