from collections import deque

from fuzzview.cfg.fv.graphnode import GraphNode
from fuzzview.cfg.fv.graphrow import GraphRow
from fuzzview.cfg.fv.pixel import EmptyPixel

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
