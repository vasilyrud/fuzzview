import os
import json

import fuzzview.const as const

class Grapher(object):

    def __init__(self, project_src_dir):
        self.project_src_dir = project_src_dir
        self.cfg_files = []

        self._find_cfg_files()
    
    def make_graphs(self, graph_class):
        graphs = []

        for cfg_file in self.cfg_files:
            with open(cfg_file) as f:
                module = json.load(f)

                graph = graph_class(module)
                graphs.append(graph)
        
        return graphs

    def _find_cfg_files(self):
        for dirpath, _, filenames in os.walk(self.project_src_dir):
            for filename in filenames:
                if filename.endswith(const.CFG_JSON_EXTENSION):
                    self.cfg_files.append(os.path.join(dirpath, filename))
        
        if not self.cfg_files:
            print('No .cfg.json files were found in ' + self.project_src_dir)
            exit(1)
