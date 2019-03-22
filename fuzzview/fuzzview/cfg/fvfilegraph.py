from collections import deque

from fuzzview.cfg.filegraph import FileGraph

class FVFileGraph(FileGraph):

    def __init__(self, module):
        super().__init__(module)

        self._generate_graph()

    def _generate_graph(self):
        for func in self._sorted_funcs():
            FuncGraph(self.module, func)

class FuncGraph(object):

    def __init__(self, module, func):
        self.module = module
        self.func = func

        # Indexed by block names
        self.nodes = {}
        
        self._generate_nodes()
        self._set_back_edges()
        self._set_shortest_depths()
        self._set_longest_depths()

        # Print nodes
        for node in self.nodes.values():
            node_width, node_height = node.get_dimensions()

            print(node.func['name'] + ':' + node.block['name'], end=', ')
            print('shortest_depth: ' + str(node.shortest_depth), end=', ')
            print('longest_depth: ' + str(node.longest_depth), end=', ')
            # print(str(node_width) + 'x' + str(node_height))
            # print(node)
            print('')

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
    
    def _set_back_edges(self):
        for src, dest in self.func['back_edges'].items():
            self.nodes[src].back_edges.add(dest)

    def _sorted_forward_next(self, cur_block):
        # back edges for cur_block
        back_edge_dests = [
            dest
            for src, dest in self.func['back_edges'].items()
            if src == cur_block['name']
        ]

        # subtract back edges from next edges
        forward_next = filter(
            lambda b_name: b_name not in back_edge_dests, 
            cur_block['next']
        )

        # sort all forward edges
        return sorted(
            forward_next, 
            key=lambda b_name: self.func['blocks'][b_name]['number']
        )

    def _set_shortest_depths(self):
        seen = set()
        q = deque()
        init_depth = 0
        q.append((init_depth, self.first_block))

        while q:
            cur = q.popleft()
            
            cur_depth = cur[0]
            cur_block = cur[1]
            cur_name  = cur_block['name']
            cur_node  = self.nodes[cur_name]

            # Save the depth in the node
            cur_node.shortest_depth = cur_depth

            for next_block_name in self._sorted_forward_next(cur_block):
                if next_block_name in seen:
                    continue

                seen.add(next_block_name)
                next_block = self.func['blocks'][next_block_name]

                q.append((cur_depth + 1, next_block))

    def _set_longest_depths(self):
        q = deque()
        init_depth = 0
        q.append((init_depth, self.first_block))

        while q:
            cur = q.popleft()

            cur_depth = cur[0]
            cur_block = cur[1]
            cur_name  = cur_block['name']
            cur_node  = self.nodes[cur_name]

            if cur_depth >= cur_node.longest_depth:
                cur_node.longest_depth = cur_depth
            
            for next_block_name in self._sorted_forward_next(cur_block):
                next_block = self.func['blocks'][next_block_name]
                q.append((cur_depth + 1, next_block))

class GraphNode(object):

    def __init__(self, module, func, block):
        self.module = module
        self.func = func
        self.block = block

        # Filled in by FuncGraph
        self.back_edges = set()
        self.shortest_depth = None
        self.longest_depth  = 0

    def get_dimensions(self):
        max_num_edges = max(
            len(self.block['prev']), 
            len(self.block['next'])
        )
        block_width = max(1, max_num_edges)

        block_height = len(self.block['calls']) + 1

        assert block_width  > 0
        assert block_height > 0

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
