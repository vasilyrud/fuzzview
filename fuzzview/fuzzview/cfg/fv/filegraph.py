from PIL import Image
import logging

from fuzzview.cfg.filegraph import FileGraph
from fuzzview.cfg.fv.funcgraph import FuncGraph
from fuzzview.cfg.fv.pixel import EmptyPixel
import fuzzview.const as const

class FVFileGraph(FileGraph):

    def __init__(self, module, cfg_file_path):
        super().__init__(module, cfg_file_path)

        # In number order
        self.func_graphs = []
        self._generate_func_graphs()

    @property
    def dimensions(self):
        return self.width, self.height

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

    def get_func_graph(self, func_name):
        for func_graph in self.func_graphs:
            if func_graph.func['name'] == func_name:
                return func_graph

        raise KeyError(func_name + ' not found in func_graphs')

    def terminal_print(self):
        pixels = self.pixels()

        count = 0
        for i in range(self.height):
            for j in range(self.width):
                print(pixels[count], end='')
                count += 1
            print('')
        print('')

    def save(self):
        pixels = [pixel.rgb for pixel in self.pixels()]

        image = Image.new('RGB', self.dimensions)
        image.putdata(pixels)
        image.save(self.save_filename + const.CFG_PNG_EXTENSION, format='PNG')

    def pixels(self):
        all_pixels = []

        for line in range(self.height):
            all_pixels += self.get_line(line)

        return all_pixels
    
    def get_line(self, line):
        pixels = []

        for graph in self.func_graphs:
            pixels += graph.get_line(line)
            pixels += [EmptyPixel()]
        
        return pixels[:-1]

    def _generate_func_graphs(self):
        logging.info('Generating ' + self.module['name'])
        for func in self._sorted_funcs():
            logging.debug('Init func_graph for function ' + func['name'])
            self.func_graphs.append(FuncGraph(self.module, func))
