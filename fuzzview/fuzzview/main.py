import argparse

from fuzzview.cfg.grapher import Grapher

def main():

    parser = argparse.ArgumentParser(description='fuzzview: fuzzing visualizer')

    args = parser.parse_args()

    Grapher()
