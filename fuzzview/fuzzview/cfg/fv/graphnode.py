import math

from fuzzview.cfg.fv.pixel import InEdgePixel, OutEdgePixel, CallPixel, NodePixel, EmptyPixel

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
                node_line += [NodePixel(self.block, self.longest_depth)] * self.only_node_width
                node_line += [CallPixel(self.block, call_func_name)]
                self.pixels.append(node_line)
        else:
            node_line = []
            node_line += [NodePixel(self.block, self.longest_depth)] * self.only_node_width
            self.pixels.append(node_line)


        if self.next_nodes:
            next_edges = []
            for node in self.next_nodes:
                next_edges += [OutEdgePixel(self.block, node)]
            next_edges += [EmptyPixel()] * (self.width - len(next_edges))
            self.pixels.append(next_edges)
