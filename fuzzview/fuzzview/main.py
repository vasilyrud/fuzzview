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
