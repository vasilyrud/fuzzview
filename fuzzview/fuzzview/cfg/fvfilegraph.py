from collections import deque
import math

from fuzzview.cfg.filegraph import FileGraph
import fuzzview.const as const

class FVFileGraph(FileGraph):

    def __init__(self, module):
        super().__init__(module)

        # In number order
        self.func_graphs = []
        self._generate_func_graphs()

        self.pixels()

    @property
    def width(self):
        # Sum of widths of all functions
        width = sum(
            (graph.width for graph in self.func_graphs)
        ) + len(self.func_graphs) - 1

        assert width > 0
        return width
    
    @property
    def height(self):
        # Max function height
        height = max(
            (graph.height for graph in self.func_graphs)
        )

        assert height > 0
        return height

    def _generate_func_graphs(self):
        for func in self._sorted_funcs():
            self.func_graphs.append(FuncGraph(self.module, func))

    def get_func_graph(self, func_name):
        for func_graph in self.func_graphs:
            if func_graph.func['name'] == func_name:
                return func_graph

        raise KeyError(func_name + ' not found in func_graphs')

    def pixels(self):
        all_pixels = []

        for line in range(self.height):
            all_pixels += self.get_line(line)

        count = 0
        for i in range(self.height):
            for j in range(self.width):
                print(all_pixels[count], end='')
                count += 1
            print('')
        print('')
    
    def get_line(self, line):
        pixels = []

        for graph in self.func_graphs:
            pixels += graph.get_line(line)
            pixels += [EmptyPixel()]
        
        return pixels[:-1]

class FuncGraph(object):

    def __init__(self, module, func):
        self.module = module
        self.func = func

        # Nodes indexed by block names
        self.nodes = {}
        # Rows indexed by depth
        self.rows = []
        # Rows indexed by line (for convenience)
        self.line_to_row = []
        # Lines within corresponding rows
        self.line_to_row_line = []

        self._generate_nodes()
        self._generate_rows()

        # print(self.func['name'])
        # print(self)

    def __str__(self):
        ret = ''
        ret += self.func['name']
        ret += '\n'
        for row in self.rows:
            ret += ' '
            ret += str(row)
            ret += '\n'

        return ret[:-1]

    def get_line(self, line):
        if line >= self.height:
            return [EmptyPixel()] * self.width

        row = self.line_to_row[line]
        row_line = self.line_to_row_line[line]

        if not row:
            return [EmptyPixel()] * self.width

        pixels = row.get_line(row_line)
        pixels += [EmptyPixel()] * (self.width - len(pixels))

        return pixels

    @property
    def width(self):
        # Max width of all rows
        width = max(
            (row.width for row in self.rows)
        )

        assert width > 0
        return width
    
    @property
    def height(self):
        # Sum of all row heights + spaces
        height = sum(
            (row.height for row in self.rows)
        ) + len(self.rows) - 1

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

        # `+1` because num_rows is used as length of array
        # into which all longest_depths should fit.
        return num_rows + 1

    def _generate_nodes(self):
        for block in self.func['blocks'].values():
            self.nodes[block['name']] = GraphNode(self.module, self.func, block)

        self._set_back_edges()
        self._set_depths()
        self._set_prev_next()
        self._generate_pixels()

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

    def _sorted_node_names(self, node_names):
        return sorted(
            node_names,
            key=lambda name: self.nodes[name].block['number']
        )

    def _set_prev_next(self):
        for node in self.nodes.values():

            for next_block_name in self._sorted_node_names(node.block['next']):
                node.next_nodes.append(self.nodes[next_block_name])
            
            for prev_block_name in self._sorted_node_names(node.block['prev']):
                node.prev_nodes.append(self.nodes[prev_block_name])

    def _generate_pixels(self):
        for node in self.nodes.values():
            node.generate_pixels()

    def _generate_rows(self):
        self.rows = [GraphRow(depth) for depth in range(self._num_rows())]

        for node in self._sorted_nodes():
            depth = node.longest_depth
            row = self.rows[depth]
            row.nodes.append(node)
        
        self.line_to_row = [None] * self.height
        self.line_to_row_line = [None] * self.height

        line = 0
        for row in self.rows:
            for row_line in range(row.height):
                self.line_to_row[line] = row
                self.line_to_row_line[line] = row_line
                line += 1
            line += 1

class GraphRow(object):

    def __init__(self, depth):
        self.depth = depth
        self.nodes = []

    def __str__(self):
        ret = ''
        for node in self.nodes:
            ret += str(node)
            ret += ' '
        
        return ret[:-1]

    @property
    def width(self):
        # Sum of all node widths + spaces
        width = sum(
            (node.width for node in self.nodes)
        ) + len(self.nodes) - 1

        assert width > 0
        return width

    @property
    def height(self):
        # Max height of nodes in the row
        height = max(
            (node.height for node in self.nodes)
        )

        assert height > 0
        return height

    def get_line(self, line):
        pixels = []

        for node in self.nodes:
            pixels += node.get_line(line)
            pixels += [EmptyPixel()]
        
        return pixels[:-1]

class GraphNode(object):

    def __init__(self, module, func, block):
        self.module = module
        self.func = func
        self.block = block

        # Filled in by FuncGraph
        self.back_edges = set()
        self.shortest_depth = math.inf
        self.longest_depth  = 0
        self.next_nodes = [] # Sorted by block number
        self.prev_nodes = [] # Sorted by block number
        self.pixels = [] # Has to be filled in last

    @property
    def dimensions(self):
        return self.width, self.height

    @property
    def width(self):
        width = self.only_node_width

        if self.block['calls']:
            width += 1

        return width

    @property
    def height(self):
        height = self.only_node_height

        if self.block['prev']:
            height += 1
        
        if self.block['next']:
            height += 1

        return height

    @property
    def only_node_dimensions(self):
        return self.only_node_width, self.only_node_height
    
    @property
    def only_node_width(self):
        max_num_edges = max(
            len(self.block['prev']), 
            len(self.block['next'])
        )
        width = max(1, max_num_edges)

        assert width > 0
        return width
    
    @property
    def only_node_height(self):
        num_calls = len(self.block['calls'])
        height = max(1, num_calls)

        assert height > 0
        return height

    def __str__(self):
        ret_str = ''

        ret_str += str(self.only_node_width)
        ret_str += 'x'
        ret_str += str(self.only_node_height)
        
        return ret_str

    def get_line(self, line):
        if line >= self.height:
            return [EmptyPixel()] * self.width
        else:
            return self.pixels[line]

    def generate_pixels(self):
        if self.prev_nodes:
            prev_edges = []
            for node in self.prev_nodes:
                prev_edges += [InEdgePixel(self.block, node)]
            prev_edges += [EmptyPixel()] * (self.width - len(prev_edges))
            self.pixels.append(prev_edges)


        if self.block['calls']:
            for call_func_name in self.block['calls']:
                node_line = []
                node_line += [NodePixel(self.block)] * self.only_node_width
                node_line += [CallPixel(self.block, call_func_name)]
                self.pixels.append(node_line)
        else:
            node_line = []
            node_line += [NodePixel(self.block)] * self.only_node_width
            self.pixels.append(node_line)


        if self.next_nodes:
            next_edges = []
            for node in self.next_nodes:
                next_edges += [OutEdgePixel(self.block, node)]
            next_edges += [EmptyPixel()] * (self.width - len(next_edges))
            self.pixels.append(next_edges)

class Pixel(object):

    def __init__(self):
        self.char = ' '
        self.color = (255,255,255)
    
    def __str__(self):
        return self.char

class InEdgePixel(Pixel):

    def __init__(self, block, src_node):
        self.char = '.'
        self.color = (0,0,0)

        self.block = block
        self.src_node = src_node

class OutEdgePixel(Pixel):

    def __init__(self, block, dest_node):
        self.char = '\''
        self.color = (0,0,0)

        self.block = block
        self.src_node = dest_node

class CallPixel(Pixel):

    def __init__(self, block, dest_func_name):
        self.char = '-'
        self.color = (0,0,0)

        self.block = block
        self.dest_func_name = dest_func_name

class NodePixel(Pixel):

    def __init__(self, block):
        self.char = '#'
        self.color = (0,0,0)

        self.block = block

class EmptyPixel(Pixel):

    def __init__(self):
        self.char = ' '
        self.color = (255,255,255)
