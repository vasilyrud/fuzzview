import argparse

from fuzzview.cfg.grapher import Grapher
from fuzzview.cfg.fv.filegraph import FVFileGraph
from fuzzview.cfg.dot.filegraph import DotFileGraph

def main():
    parser = argparse.ArgumentParser(
        description='fuzzview: fuzzing visualizer')

    parser.add_argument('project_src_dir', 
        help='Directory containing project source files.')

    args = parser.parse_args()

    grapher = Grapher(args.project_src_dir)
    grapher.make_graphs(DotFileGraph)
    grapher.make_graphs(FVFileGraph)
