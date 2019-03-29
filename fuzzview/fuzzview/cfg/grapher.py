import os
import json
import logging

import fuzzview.const as const

class DirGrapher(object):

    def __init__(self, project_src_dir):
        self.project_src_dir = project_src_dir
        self.file_graphers = []

        self._find_cfg_files()
    
    def save_graphs(self, graph_class):
        for file_grapher in self.file_graphers:
            file_grapher.save_graph(graph_class)

    def _find_cfg_files(self):
        for dirpath, _, filenames in os.walk(self.project_src_dir):
            for filename in filenames:
                if filename.endswith(const.CFG_JSON_EXTENSION):
                    file_grapher = FileGrapher(os.path.join(dirpath, filename))
                    self.file_graphers.append(file_grapher)
        
        if not self.file_graphers:
            print('No .cfg.json files were found in ' + self.project_src_dir)
            exit(1)

class FileGrapher(object):

    def __init__(self, cfg_filename):
        self.cfg_filename = cfg_filename
    
    def save_graph(self, graph_class):
        with open(self.cfg_filename) as f:
            module = json.load(f)
            graph = graph_class(module, self.cfg_filename)
            
            # graph.terminal_print()
            graph.save()
