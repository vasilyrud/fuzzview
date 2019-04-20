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
import logging

import fuzzview.const as const

class DirGrapher(object):
    ''' Creates graphs for all cfg files in a
    directory and all its sub-directories.

    Attributes:
        project_src_dir: Top directory within which all
            CFG files are found recursively.
        file_graphers: FileGrapher objects for each file.
    '''

    def __init__(self, project_src_dir):

        self.project_src_dir = project_src_dir
        self.file_graphers = []

        self._find_cfg_files()
    
    def save_graphs(self, graph_class):
        ''' Save graphs for all files.
        '''

        for file_grapher in self.file_graphers:
            file_grapher.save_graph(graph_class)

    def _find_cfg_files(self):
        ''' Look through all subdirs with os.walk
        and create FileGrapher objects for each file.
        '''

        for dirpath, _, filenames in os.walk(self.project_src_dir):
            for filename in filenames:
                if filename.endswith(const.CFG_JSON_EXTENSION):
                    file_grapher = FileGrapher(os.path.join(dirpath, filename))
                    self.file_graphers.append(file_grapher)
        
        if not self.file_graphers:
            print('No .cfg.json files were found in ' + self.project_src_dir)
            sys.exit(1)

class FileGrapher(object):
    ''' Creates graphs for a given file.

    Attributes:
        cfg_filename: Full filename for which
            the graph is to be created (string).
    '''

    def __init__(self, cfg_filename):

        self.cfg_filename = cfg_filename
    
    def save_graph(self, graph_class):
        ''' Save graph for cfg_filename using the
        graph_class to create the graph.

        Args:
            graph_class: A class derived from FileGraph
                that implements the save() method.
        '''

        with open(self.cfg_filename) as f:
            module = json.load(f)
            graph = graph_class(module, self.cfg_filename)
            
            # graph.terminal_print()
            graph.save()
            graph.save_funcs()
