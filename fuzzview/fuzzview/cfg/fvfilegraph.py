from collections import deque
import math

from fuzzview.cfg.filegraph import FileGraph
import fuzzview.const as const

class FVFileGraph(FileGraph):

    def __init__(self, module):
        super().__init__(module)

        # Indexed by func names
        self.func_graphs = {}

        self._generate_graph()

    def _generate_graph(self):
        for func in self._sorted_funcs():
            self.func_graphs[func['name']] = FuncGraph(self.module, func)

class FuncGraph(object):

    def __init__(self, module, func):
        self.module = module
        self.func = func

        # Indexed by block names
        self.nodes = {}
        
        self._generate_nodes()
        self._set_back_edges()
        self._set_depths()

        # Print nodes
        for node in self.nodes.values():
            # print(node.func['name'] + ':' + node.block['name'], end=', ')
            # print('shortest_depth: ' + str(node.shortest_depth), end=', ')
            # print('longest_depth: ' + str(node.longest_depth), end=', ')
            # print(str(node.width) + 'x' + str(node.height))
            # print(node)
            # print('')
            continue
        
        self.rows = [[] for _ in range(self._num_rows())]
        for node in self._sorted_nodes():
            self.rows[node.longest_depth].append(node)
        
        # print([len(row) for row in self.rows])
        # print(self.width, self.height)
        print(self.func['name'])
        print(self)

    def __str__(self):
        ret = ''

        for row in self.rows:
            # print row
            for line in range(self._row_height(row)):
                line_str = ''
                for node in row:
                    line_str += node.str_line(line)
                    line_str += const.EMPTY_CHAR
                line_str = line_str[:-1]

                assert len(line_str) == self._row_width(row)

                ret += line_str
                ret += '\n'
            ret += '\n'
        
        return ret

    @property
    def width(self):
        # Max width of all rows
        width = max(
            (self._row_width(row) for row in self.rows)
        )

        assert width > 0
        return width
    
    @property
    def height(self):
        # Sum of all row heights + spaces
        height = sum(
            (self._row_height(row) for row in self.rows)
        ) + len(self.rows) - 1

        assert height > 0
        return height

    def _row_width(self, row):
        # Sum of all node widths + spaces
        width = sum(
            (node.width for node in row)
        ) + len(row) - 1

        assert width > 0
        return width

    def _row_height(self, row):
        # Max height of nodes in the row
        height = max(
            (node.height for node in row)
        )

        assert height > 0
        return height

    @property
    def first_block(self):
        first_block = min(
            self.func['blocks'].values(),
            key=lambda f: f['number']
        )

        assert not first_block['prev']
        return first_block

    def _sorted_nodes(self):
        return sorted(
            self.nodes.values(),
            key=lambda node: node.block['number']
        )

    def _num_rows(self):
        # Largest longest_depth
        num_rows = max(map(
            lambda node: node.longest_depth, 
            self.nodes.values()
        ))

        # `+ 1` because num_rows is used as length of array
        # into which all longest_depths should fit.
        return num_rows + 1

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

    def _set_depths(self):
        q = deque()
        init_depth = 0
        q.append((init_depth, self.first_block))

        while q:
            cur = q.popleft()
            
            cur_depth = cur[0]
            cur_block = cur[1]
            cur_name  = cur_block['name']
            cur_node  = self.nodes[cur_name]

            if cur_depth < cur_node.shortest_depth:
                cur_node.shortest_depth = cur_depth
            
            if cur_depth > cur_node.longest_depth:
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
        self.shortest_depth = math.inf
        self.longest_depth  = 0

    @property
    def dimensions(self):
        return self.width, self.height

    @property
    def width(self):
        max_num_edges = max(
            len(self.block['prev']), 
            len(self.block['next'])
        )
        
        width = max(1, max_num_edges)
        
        assert width  > 0
        return width

    @property
    def height(self):
        height = len(self.block['calls']) + 1

        assert height > 0
        return height

    def __repr__(self):
        return str(self)

    def __str__(self):
        ret_str = ''

        ret_str += str(self.width)
        ret_str += 'x'
        ret_str += str(self.height)
        
        return ret_str
    
    def str_line(self, line):
        if line >= self.height:
            return const.EMPTY_CHAR * self.width
        else:
            return const.NODE_CHAR * self.width
