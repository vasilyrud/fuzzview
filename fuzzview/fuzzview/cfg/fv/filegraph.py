from PIL import Image
import logging
import os

from fuzzview.cfg.filegraph import FileGraph
from fuzzview.cfg.fv.funcgraph import FuncGraph
from fuzzview.cfg.fv.pixel import EmptyPixel
import fuzzview.const as const

class FVFileGraph(FileGraph):
    ''' fuzzview-specific graph generator.

    Used to create image files with the pixel-based
    fuzzview representation of the file's cfg.

    The graph is composed of multiple FuncGraphs, that
    contain graphs for individual functions.

    Attributes:
        func_graphs: All the fuzzview graphs for 
            functions in this file, sorted in the 
            order that they appear in in the file.
    '''

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
        ''' Fetch a FuncGraph by name.
        '''

        for func_graph in self.func_graphs:
            if func_graph.func['name'] == func_name:
                return func_graph

        raise KeyError(func_name + ' not found in func_graphs')

    def terminal_print(self):
        ''' Quickly print the pixels to terminal.
        May overflow terminal width.
        '''

        pixels = self.pixels()

        count = 0
        for i in range(self.height):
            for j in range(self.width):
                print(pixels[count], end='')
                count += 1
            print('')
        print('')

    def save_funcs(self):
        ''' Save the images produced by individual functions
        to a dir.
        '''

        func_images_dir = self.save_filename + '_' + const.FV_FUNC_IMG_DIR
        os.makedirs(func_images_dir, exist_ok=True)

        for func_graph in self.func_graphs:
            func_graph.save(func_images_dir)

    def save(self):
        ''' Save the image produced by this class to a file.
        '''

        pixels = [pixel.rgb for pixel in self.pixels()]

        image = Image.new('RGB', self.dimensions)
        image.putdata(pixels)
        image.save(self.save_filename + const.FILE_PNG_EXTENSION, format='PNG')

    def pixels(self):
        ''' Collect all the lines into a single continuous
        pixel array, which is the format that PIL expects.
        '''
 
        all_pixels = []

        for line in range(self.height):
            all_pixels += self.get_line(line)

        return all_pixels

    def get_line(self, line):
        ''' Collect pixels for a single line of
        the image.
        '''

        pixels = []

        for graph in self.func_graphs:
            pixels += graph.get_line(line)
            pixels += [EmptyPixel()]
        
        return pixels[:-1]

    def _generate_func_graphs(self):
        ''' Initializes the graphs of individual functions
        in the file.
        '''

        logging.info('Generating ' + self.module['name'])
        for func in self._sorted_funcs():

            logging.debug('Init func_graph for function ' + func['name'])
            self.func_graphs.append(FuncGraph(self.module, func))
