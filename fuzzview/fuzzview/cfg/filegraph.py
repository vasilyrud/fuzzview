import os

import fuzzview.const as const

class FileGraph(object):

    def __init__(self, module, cfg_file_path):
        self.module = module

        # Location of .cfg.json file (rather than 
        # the location of .c source file).
        self.cfg_dirpath, self.cfg_filename_with_ext = os.path.split(cfg_file_path)
        ext_len = len(const.CFG_JSON_EXTENSION)
        self.cfg_filename = self.cfg_filename_with_ext[:-ext_len]

    def save(self):
        pass
    
    def terminal_print(self):
        pass

    @property
    def source_filename(self):
        return (
            self.module['path'] + '/' + 
            self.module['name']
        )
    
    @property
    def save_filename(self):
        return (
            self.cfg_dirpath + '/' +
            self.cfg_filename
        )

    def _sorted_funcs(self):
        return sorted(
            self.module['functions'].values(),
            key=lambda f: f['number']
        )
    
    def _block_id(self, func, block):
        return (
            self.module['path'] + '/' + 
            self.module['name'] + '.' + 
            func['name'] + '.' +
            block['name']
        )
