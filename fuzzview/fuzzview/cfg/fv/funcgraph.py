from collections import deque
import logging

from fuzzview.cfg.fv.graphnode import GraphNode
from fuzzview.cfg.fv.graphrow import GraphRow
from fuzzview.cfg.fv.pixel import EmptyPixel

class FuncGraph(object):
    ''' Per-function graph.

    Attributes:
        module: A module object produced by the LLVM
            FvPass, containing the CFGs of all the
            functions in a file.
        func: An object inside self.module for a specific
            function in the file.
        nodes: Nodes of the graph (blocks) indexed by 
            block names (string).
    '''

    def __init__(self, module, func):

        self.module = module
        self.func = func
        self.nodes = {}

        # Rows indexed by depth
        self._rows = []
        # Rows indexed by line (for convenience)
        self._line_to_row = []
        # Lines within corresponding rows
        self._line_to_row_line = []

        self._generate_nodes()
        self._generate_rows()

    def __str__(self):

        ret = ''
        ret += self.func['name']
        ret += '\n'
        for row in self._rows:
            ret += ' '
            ret += str(row)
            ret += '\n'

        return ret[:-1]

    def get_line(self, line):
        ''' Get line of pixels for the func, or
        a line of empty pixels if line number is
        out of bounds.

        Args:
            line: Which line of pixels to get.
        '''

        if line >= self.height:
            return [EmptyPixel()] * self.width

        row = self._line_to_row[line]
        row_line = self._line_to_row_line[line]

        if not row:
            return [EmptyPixel()] * self.width

        pixels = row.get_line(row_line)
        pixels += [EmptyPixel()] * (self.width - len(pixels))

        return pixels

    @property
    def width(self):

        # Max width of all rows
        width = max(
            (row.width for row in self._rows)
        )

        assert width > 0
        return width
    
    @property
    def height(self):

        # Sum of all row heights + spaces
        height = sum(
            (row.height for row in self._rows)
        ) + len(self._rows) - 1

        assert height > 0
        return height

    @property
    def first_block(self):
        ''' Returns first block CFG object.
        '''

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
        ''' Determines the number or GraphRows needed
        to hold the function CFG.
        '''

        # Largest longest_depth
        num_rows = max(map(
            lambda node: node.longest_depth, 
            self.nodes.values()
        ))

        # `+1` because num_rows is used as length of array
        # into which all longest_depths should fit.
        return num_rows + 1

    def _generate_nodes(self):
        ''' Creates all GraphNodes and initializes
        GraphNode attributes.
        '''

        for block in self.func['blocks'].values():
            self.nodes[block['name']] = GraphNode(self.module, self.func, block)

        self._set_back_edges()
        self._set_depths()
        self._set_prev_next()
        self._generate_pixels()

    def _set_back_edges(self):
        ''' Back edges are found during the LLVM pass,
        so this adds them to the relevant GraphNodes.
        '''

        for src, dest in self.func['back_edges'].items():
            self.nodes[src].back_edges.add(dest)

    def _sorted_forward_next(self, cur_block):
        ''' All the next blocks from a current block,
        sorted by the order in which they appear in the
        LLVM IR, with any back edges subtracted.
        '''

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

    def _update_shortest(self, cur_depth, cur_node):
        ''' Whether a new shortest path was found.
        '''

        if cur_depth < cur_node.shortest_depth:
            cur_node.shortest_depth = cur_depth
            return True
        
        return False

    def _update_longest(self, cur_depth, cur_node):
        ''' Whether a new longest path was found.
        '''

        if cur_depth > cur_node.longest_depth:
            cur_node.longest_depth = cur_depth
            return True
        
        return False

    def _set_depths(self):
        ''' Find the lengths of both shortest and 
        longest paths to each block by doing a BFS 
        through all the blocks in the CFG of the 
        function.
        '''

        q = deque()
        init_depth = 0
        q.append((init_depth, self.first_block))

        while q:
            cur = q.popleft()
            
            cur_depth = cur[0]
            cur_block = cur[1]
            cur_name  = cur_block['name']
            cur_node  = self.nodes[cur_name]

            shortest_updated = self._update_shortest(cur_depth, cur_node)
            longest_updated  = self._update_longest(cur_depth, cur_node)

            if (not shortest_updated and
                not longest_updated):
                continue

            for next_block_name in self._sorted_forward_next(cur_block):
                next_block = self.func['blocks'][next_block_name]
                q.append((cur_depth + 1, next_block))

    def _sorted_node_names(self, node_names):

        return sorted(
            node_names,
            key=lambda name: self.nodes[name].block['number']
        )

    def _set_prev_next(self):
        ''' Link nodes together after they have all 
        been created.
        '''

        for node in self.nodes.values():

            for next_block_name in self._sorted_node_names(node.block['next']):
                node.next_nodes.append(self.nodes[next_block_name])
            
            for prev_block_name in self._sorted_node_names(node.block['prev']):
                node.prev_nodes.append(self.nodes[prev_block_name])

    def _generate_pixels(self):
        ''' Create pixels for each node.
        '''

        for node in self.nodes.values():
            node.generate_pixels()

    def _generate_rows(self):
        ''' Create GraphRow objects and add GraphNodes
        to their corresponding GraphRow.
        '''

        self._rows = [GraphRow(depth) for depth in range(self._num_rows())]

        for node in self._sorted_nodes():
            depth = node.longest_depth
            row = self._rows[depth]
            row.nodes.append(node)
        
        self._line_to_row = [None] * self.height
        self._line_to_row_line = [None] * self.height

        line = 0
        for row in self._rows:
            for row_line in range(row.height):
                self._line_to_row[line] = row
                self._line_to_row_line[line] = row_line
                line += 1
            line += 1
