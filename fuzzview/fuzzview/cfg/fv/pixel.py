import colorsys

class Pixel(object):

    def __init__(self):
        self.char = ' '
        self.rgb = (255,255,255)
    
    def __str__(self):
        return self.char

class InEdgePixel(Pixel):

    def __init__(self, block, src_node):
        self.char = '.'
        self.rgb = (0,0,0)

        self.block = block
        self.src_node = src_node

class OutEdgePixel(Pixel):

    def __init__(self, block, dest_node):
        self.char = '\''
        self.rgb = (0,0,0)

        self.block = block
        self.src_node = dest_node

class CallPixel(Pixel):

    def __init__(self, block, dest_func_name):
        self.char = '-'
        self.rgb = (0,0,0)

        self.block = block
        self.dest_func_name = dest_func_name

class NodePixel(Pixel):

    def __init__(self, block, depth):
        self.char = '#'
        # self.rgb = (0,0,0)

        self.block = block
        self.depth = depth
    
    @property
    def rgb(self):
        max_depth = 30
        hue = self.depth/max_depth
        if hue > 1.0:
            hue = 1.0
        rgb_ratio = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        r_float, g_float, b_float = rgb_ratio[0]*255, rgb_ratio[1]*255, rgb_ratio[2]*255
        r, g, b = int(r_float), int(g_float), int(b_float)
        return r, g, b

class EmptyPixel(Pixel):

    def __init__(self):
        self.char = ' '
        self.rgb = (255,255,255)
