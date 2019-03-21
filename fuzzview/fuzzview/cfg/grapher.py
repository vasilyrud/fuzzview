import os
import json
from collections import deque

import fuzzview.const as const

class Grapher(object):

    def __init__(self, project_src_dir):
        self.project_src_dir = project_src_dir
        self.cfg_files = []
        self.graphs = []

        self._find_cfg_files()
    
    def generate_all_graphs(self):
        for cfg_file in self.cfg_files:
            with open(cfg_file) as f:
                module = json.load(f)
                self._generate_file_graphs(module)

    def _find_cfg_files(self):
        for dirpath, _, filenames in os.walk(self.project_src_dir):
            for filename in filenames:
                if filename.endswith(const.CFG_FILE_EXTENSION):
                    self.cfg_files.append(os.path.join(dirpath, filename))

    def _sorted_funcs(self, funcs_obj):
        return sorted(
            funcs_obj.values(), 
            key=lambda f: f['number']
        )

    def _generate_file_graphs(self, module):
        for func in self._sorted_funcs(module['functions']):
            func_graph = FuncGraph(module, func)

class FuncGraph(object):

    def __init__(self, module, func):
        self.module = module
        self.func = func

        # Indexed by block names
        self.nodes = {}
        
        self._generate_nodes()
        self._set_bfs_depths()

        # Print nodes
        for node in self.nodes.values():
            node_width, node_height = node.get_dimensions()

            print(node.func['name'] + ':' + node.block['name'])
            print('bfs_depth: ' + str(node.bfs_depth))
            print(str(node_width) + 'x' + str(node_height))
            print(node)

    @property
    def first_block(self):
        return self._first_block()

    def _first_block(self):
        first_block = min(
            self.func['blocks'].values(),
            key=lambda f: f['number']
        )

        assert not first_block['prev']
        return first_block

    def _generate_nodes(self):
        for block in self.func['blocks'].values():
            self.nodes[block['name']] = GraphNode(self.module, self.func, block)
    
    def _set_bfs_depths(self):
        seen = set()
        q = deque()
        depth_counter = 0
        q.append((depth_counter, self.first_block))

        while q:
            cur = q.popleft()
            
            cur_depth = cur[0]
            cur_block = cur[1]
            cur_node  = self.nodes[cur_block['name']]
            depth_counter = cur_depth + 1

            # Save the depth in the node
            cur_node.bfs_depth = cur_depth

            for next_block_name in sorted(cur_block['next']):
                if next_block_name in seen:
                    continue

                seen.add(next_block_name)
                next_block = self.func['blocks'][next_block_name]

                q.append((depth_counter, next_block))

class GraphNode(object):

    def __init__(self, module, func, block):
        self.module = module
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
