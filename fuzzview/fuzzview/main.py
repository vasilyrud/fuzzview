import argparse

from fuzzview.cfg.grapher import Grapher
from fuzzview.cfg.fv.filegraph import FVFileGraph
from fuzzview.cfg.dot.filegraph import DotFileGraph

def generate_dot_graphs(grapher):
    dot_graphs = grapher.make_graphs(DotFileGraph)
    for dot_graph in dot_graphs:
        dot_graph.save()

def generate_fv_graphs(grapher):
    fv_graphs = grapher.make_graphs(FVFileGraph)
    for fv_graph in fv_graphs:
        fv_graph.terminal_print()
        fv_graph.save()

def main():
    parser = argparse.ArgumentParser(
        description='fuzzview: fuzzing visualizer')

    parser.add_argument('project_src_dir', 
        help='Directory containing project source files.')

    args = parser.parse_args()

    grapher = Grapher(args.project_src_dir)

    generate_dot_graphs(grapher)
    generate_fv_graphs(grapher)
