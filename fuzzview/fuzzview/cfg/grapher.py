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

    def generate_all_graphs(self):

        for cfg_file in self.cfg_files:
            with open(cfg_file) as f:
                cfg = json.load(f)
                self._generate_file_graphs(cfg)

    def _sorted_funcs(self, funcs_obj):
        return sorted(
            funcs_obj.items(), 
            key=lambda f: f[1]['number']
        )

    def _generate_file_graphs(self, cfg):

        for func_name, func in self._sorted_funcs(cfg['functions']):
            self._generate_func_graph(func_name, func)

    def _min_block(self, blocks_obj):
        return min(
            blocks_obj.items(),
            key=lambda f: f[1]['number']
        )

    def _get_node_dimensions(self, block):
        
        max_num_edges = max(
            len(block['prev']), 
            len(block['next'])
        )
        block_width = max(1, max_num_edges)

        block_height = len(block['calls']) + 1

        return block_width, block_height

    def _print_node(self, node):

        for i in range(len(node)):
            for j in range(len(node[0])):
                print('#', end='')
            print('')

    def _generate_func_graph(self, func_name, func):

        first_block_id, first_block = self._min_block(func['blocks'])
        assert not first_block['prev']

        block_width, block_height = self._get_node_dimensions(first_block)

        block_node = [['.' for j in range(block_width)] for i in range(block_height)]

        print(func_name + ':' + first_block_id)
        print(str(block_width) + 'x' + str(block_height))
        self._print_node(block_node)
        print('')
