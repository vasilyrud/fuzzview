import os

import fuzzview.const as const

class Grapher(object):

    def __init__(self, project_src_dir):

        self.project_src_dir = project_src_dir

        self._find_cfg_files()

    def _find_cfg_files(self):

        self.cfg_files = []

        for dirpath, _, filenames in os.walk(self.project_src_dir):
            for filename in filenames:
                if filename.endswith(const.CFG_FILE_EXTENSION):
                    self.cfg_files.append(os.path.join(dirpath, filename))

        print(self.cfg_files)
