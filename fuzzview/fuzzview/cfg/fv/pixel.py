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

    def __init__(self, block):
        self.char = '#'
        self.rgb = (0,0,0)

        self.block = block

class EmptyPixel(Pixel):

    def __init__(self):
        self.char = ' '
        self.rgb = (255,255,255)
