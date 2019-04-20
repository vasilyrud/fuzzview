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

import colorsys
from palettable.matplotlib import Plasma_20

class Pixel(object):
    ''' Single pixel in a graph.

    Useful because graphs can be rendered on
    different mediums.

    Attributes:
        char: Single character representation.
        rgb: Color of the pixel as a triple.
        block: The CFG block which the pixel is
            part of (if any).
    '''

    char = ' '
    rgb = (255, 255, 255)

    def __init__(self):
        pass

    def __str__(self):
        return self.char

class InEdgePixel(Pixel):

    char = '.'
    rgb = (0,0,0)

    def __init__(self, block, src_node):
        self.block = block
        self.src_node = src_node

class OutEdgePixel(Pixel):

    char = '\''
    rgb = (0,0,0)

    def __init__(self, block, dest_node):
        self.block = block
        self.src_node = dest_node

class CallPixel(Pixel):

    char = '-'
    rgb = (0,0,0)

    def __init__(self, block, dest_func_name):
        self.block = block
        self.dest_func_name = dest_func_name

class NodePixel(Pixel):

    char = '#'
    # rgb = (0,0,0)

    def __init__(self, block, depth):
        self.block = block
        self.depth = depth

    @property
    def rgb(self):
        colors = Plasma_20.mpl_colors
        depth = self.depth

        if depth > len(colors) - 1:
            depth = len(colors) - 1
        color = colors[depth]

        return tuple(map(lambda v: int(v*255), color))

        # max_depth = 30
        # hue = self.depth/max_depth
        # if hue > 1.0:
        #     hue = 1.0
        # rgb_ratio = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        # r_float, g_float, b_float = rgb_ratio[0]*255, rgb_ratio[1]*255, rgb_ratio[2]*255
        # r, g, b = int(r_float), int(g_float), int(b_float)
        # return r, g, b

class EmptyPixel(Pixel):
    char = ' '
    rgb = (255,255,255)
