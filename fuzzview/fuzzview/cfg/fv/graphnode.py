import math

from fuzzview.cfg.fv.pixel import InEdgePixel, OutEdgePixel, CallPixel, NodePixel, EmptyPixel

class GraphNode(object):
    ''' Nodes in a function graph.

    Each node corresponds to a basic block in LLVM IR.

    Attributes:
        module: A module object produced by the LLVM
            FvPass, containing the CFGs of all the
            functions in a file.
        func: A function object in the CFG to which the 
            node belongs.
        block: The block object for this node in the CFG.
        back_edges: Any next edges that are back edges in
            the CFG.
        shortest_depth: Length of shortest path starting 
            from the first block of the function.
        longest_depth: Length of longest path starting
            from the first block of the function.
        next_nodes: GraphNodes that follow this node.
        prev_nodes: GraphNodes that precede this node.
    '''

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

        # Has to be filled in last with call to generate_pixels()
        self._pixels = []

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
        ''' Dimensions without edges and without calls.
        '''

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
        ''' Returns line of pixels.
        '''

        if line >= self.height:
            return [EmptyPixel()] * self.width
        else:
            return self._pixels[line]

    def generate_pixels(self):
        ''' Generate pixels for this node by first including
        incoming edges, then adding pixels for lines with calls,
        and finally drawing outgoing edges.

        This function should be called last, after all attributes
        of the GraphNode have been initialized.
        '''

        # incoming edges
        if self.prev_nodes:
            prev_edges = []

            for node in self.prev_nodes:
                prev_edges += [InEdgePixel(self.block, node)]

            prev_edges += [EmptyPixel()] * (self.width - len(prev_edges))
            self._pixels.append(prev_edges)


        # calls
        if self.block['calls']:

            for call_func_name in self.block['calls']:
                node_line = []
                node_line += [NodePixel(self.block, self.longest_depth)] * self.only_node_width
                node_line += [CallPixel(self.block, call_func_name)]
                self._pixels.append(node_line)
        else:
            node_line = []
            node_line += [NodePixel(self.block, self.longest_depth)] * self.only_node_width
            self._pixels.append(node_line)


        # outgoing edges
        if self.next_nodes:
            next_edges = []

            for node in self.next_nodes:
                next_edges += [OutEdgePixel(self.block, node)]

            next_edges += [EmptyPixel()] * (self.width - len(next_edges))
            self._pixels.append(next_edges)
