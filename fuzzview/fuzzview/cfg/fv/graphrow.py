# Copyright 2019 Vasily Rudchenko - Fuzzview
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fuzzview.cfg.fv.graphnode import GraphNode
from fuzzview.cfg.fv.pixel import EmptyPixel

class GraphRow(object):
    ''' Rows in a function graph.

    Each row corresponds to several nodes, combined
    together based on their depth. 

    Attributes:
        depth: A depth of the node (block) within the function.
            This could be, for example, the length of
            the shortest path to the node, or the length
            of the longest path.
        nodes: GraphNodes on this row.
    '''

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
        ''' Returns the pixels on the particular
        line of this row.
        '''

        pixels = []

        for node in self.nodes:
            pixels += node.get_line(line)
            pixels += [EmptyPixel()]
        
        return pixels[:-1]
