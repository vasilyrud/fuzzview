import argparse
import logging

from fuzzview.cfg.grapher import DirGrapher, FileGrapher
from fuzzview.cfg.fv.filegraph import FVFileGraph
from fuzzview.cfg.dot.filegraph import DotFileGraph

def main():
    parser = argparse.ArgumentParser(
        description='fuzzview: fuzzing visualizer')

    parser.add_argument('json_source_type',
        help='How to get the json files.', choices=['dir', 'file'])
    parser.add_argument('json_source', 
        help='Directory containing project source files or a file itself.')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    if args.json_source_type == 'dir':

        dir_grapher = DirGrapher(args.json_source)
        # dir_grapher.save_graphs(DotFileGraph)
        dir_grapher.save_graphs(FVFileGraph)

    elif args.json_source_type == 'file':

        file_grapher = FileGrapher(args.json_source)
        file_grapher.save_graph(FVFileGraph)
