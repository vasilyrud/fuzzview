import os

import fuzzview.const as const

class FileGraph(object):
    ''' Base calls for file-level graph generators.

    Derived classes may want to implement:
        save: In order to write out the graph to
            the same dir as the source file.
        terminal_print: In order to see a rough 
            version of the graph in terminal.

    Attributes:
        module: A module object produced by the LLVM
            FvPass, containing the CFGs of all the
            functions in a file.
        source_filename: Full filename of the source file
            based on which the CFG file was generated.
        save_filename: Full filename of the CFG file, but 
            without the extension.
    '''

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
        ''' Functions sorted by the order in which
        they appear in the LLVM IR.
        '''

        return sorted(
            self.module['functions'].values(),
            key=lambda f: f['number']
        )
    
    def _block_id(self, func, block):
        ''' Helper function that provides a
        unique identifier for a given LLVM block
        in a CFG.
        '''

        return (
            self.module['path'] + '/' + 
            self.module['name'] + '.' + 
            func['name'] + '.' +
            block['name']
        )
