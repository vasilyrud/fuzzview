import os
import json

import fuzzview.const as const

class Grapher(object):

    def __init__(self, project_src_dir):

        self.project_src_dir = project_src_dir
        self.cfg_files = []

        self._find_cfg_files()

    def _find_cfg_files(self):

        for dirpath, _, filenames in os.walk(self.project_src_dir):
            for filename in filenames:
                if filename.endswith(const.CFG_FILE_EXTENSION):
                    self.cfg_files.append(os.path.join(dirpath, filename))

    def generate_graphs(self):

        for cfg_file in self.cfg_files:
            with open(cfg_file) as f:
                cfg = json.load(f)
                self._generate_graph(cfg)

    def _generate_graph(self, cfg):

        print(cfg['functions'].keys())
