import argparse

from fuzzview.cfg.grapher import Grapher

def main():
    parser = argparse.ArgumentParser(
        description='fuzzview: fuzzing visualizer')

    parser.add_argument('project_src_dir', 
        help='Directory containing project source files.')

    args = parser.parse_args()

    grapher = Grapher(args.project_src_dir)
    grapher.make_graphs('dot')
    grapher.make_graphs('fuzzview')
