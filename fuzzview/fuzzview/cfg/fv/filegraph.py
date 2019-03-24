from fuzzview.cfg.filegraph import FileGraph
from fuzzview.cfg.fv.funcgraph import FuncGraph
from fuzzview.cfg.fv.pixel import EmptyPixel
import fuzzview.const as const

class FVFileGraph(FileGraph):

    def __init__(self, module):
        super().__init__(module)

        # In number order
        self.func_graphs = []
        self._generate_func_graphs()

        self.pixels()

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

    def _generate_func_graphs(self):
        for func in self._sorted_funcs():
            self.func_graphs.append(FuncGraph(self.module, func))

    def get_func_graph(self, func_name):
        for func_graph in self.func_graphs:
            if func_graph.func['name'] == func_name:
                return func_graph

        raise KeyError(func_name + ' not found in func_graphs')

    def pixels(self):
        all_pixels = []

        for line in range(self.height):
            all_pixels += self.get_line(line)

        count = 0
        for i in range(self.height):
            for j in range(self.width):
                print(all_pixels[count], end='')
                count += 1
            print('')
        print('')
    
    def get_line(self, line):
        pixels = []

        for graph in self.func_graphs:
            pixels += graph.get_line(line)
            pixels += [EmptyPixel()]
        
        return pixels[:-1]
