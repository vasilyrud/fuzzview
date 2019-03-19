import os
import json

import fuzzview.const as const

class GraphNode(object):

    def __init__(self, cfg, func, block):
        self.cfg = cfg
        self.func = func
        self.block = block

    def get_dimensions(self):
        
        max_num_edges = max(
            len(self.block['prev']), 
            len(self.block['next'])
        )
        block_width = max(1, max_num_edges)

        block_height = len(self.block['calls']) + 1

        return block_width, block_height

    def __str__(self):

        ret_str = ''

        block_width, block_height = self.get_dimensions()
        grid = [['.' for j in range(block_width)] for i in range(block_height)]

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                ret_str += '#'
            ret_str += '\n'
        
        return ret_str

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

    def generate_all_graphs(self):

        for cfg_file in self.cfg_files:
            with open(cfg_file) as f:
                cfg = json.load(f)
                self._generate_file_graphs(cfg)

    def _sorted_funcs(self, funcs_obj):
        return sorted(
            funcs_obj.values(), 
            key=lambda f: f['number']
        )

    def _generate_file_graphs(self, cfg):

        for func in self._sorted_funcs(cfg['functions']):
            self._generate_func_graph(cfg, func)

    def _min_block(self, blocks_obj):
        return min(
            blocks_obj.values(),
            key=lambda f: f['number']
        )

    def _generate_func_graph(self, cfg, func):

        first_block = self._min_block(func['blocks'])
        assert not first_block['prev']

        first_node = GraphNode(cfg, func, first_block)

        block_width, block_height = first_node.get_dimensions()

        print(func['name'] + ':' + first_block['name'])
        print(str(block_width) + 'x' + str(block_height))
        print(first_node)
