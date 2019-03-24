import subprocess

import fuzzview.const as const
from fuzzview.cfg.filegraph import FileGraph

class DotFileGraph(FileGraph):

    def __init__(self, module):
        super().__init__(module)

        self.graph = self._generate_graph()
    
    def save(self):
        self._save_dot()
        self._save_pdf()

    def _save_dot(self):
        dot_filename = self.filename + const.CFG_DOT_EXTENSION

        with open(dot_filename, 'w') as f:
            f.write(self.graph)

    def _save_pdf(self):
        dot_filename = self.filename + const.CFG_DOT_EXTENSION
        pdf_filename = self.filename + const.CFG_PDF_EXTENSION

        cmd = 'dot -Tpdf ' + dot_filename + ' -o ' + pdf_filename
        
        subprocess.run(
            cmd.split(' ')
        )

    def _generate_graph(self):
        ret = ''
        ret += 'digraph G {\n'

        for func in self._sorted_funcs():
            ret += self._make_func_graph(func)

        ret += '}\n'

        return ret

    def _make_call_info(self, call):
        ret = ''

        if call['type'] == 'direct':
            ret += call['function']
        else:
            ret += 'indirect: '
            ret += call['signature']
        
        return ret

    def _make_label(self, block):
        ret = ''
        ret += block['name']
        ret += '\n'

        for call in block['calls']:
            ret += self._make_call_info(call)
            ret += '\n'

        ret = ret.rstrip('\n')

        return ret

    def _make_block_node(self, func, block):
        ret = ''
        ret += '\t"'
        ret += self._block_id(func, block)
        ret += '" ['
        ret += 'label="' + self._make_label(block) + '"'
        ret += '];\n'
        
        for nxt_block_name in block['next']:
            ret += '\t"'
            ret += self._block_id(func, block)
            ret += '" -> "'
            ret += self._block_id(func, func['blocks'][nxt_block_name])
            ret += '";\n'
        
        return ret

    def _make_func_cluster(self, func):
        ret = ''
        ret += '\tsubgraph "cluster' + func['name'] + '" {\n'
        ret += '\t\tlabel="' + func['name'] + '";\n'
        
        for block in func['blocks'].values():

            ret += '\t\t"'
            ret += self._block_id(func, block)
            ret += '";\n'

        ret += '\t}\n'
        
        return ret

    def _make_func_graph(self, func):
        ret = ''

        for block in func['blocks'].values():
            ret += self._make_block_node(func, block)

        ret += self._make_func_cluster(func)

        return ret
