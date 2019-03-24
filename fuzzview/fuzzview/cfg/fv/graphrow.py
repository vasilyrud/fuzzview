from fuzzview.cfg.fv.graphnode import GraphNode
from fuzzview.cfg.fv.pixel import EmptyPixel

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
