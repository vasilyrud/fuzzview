
class FileGraph(object):

    def __init__(self, module):
        self.module = module

    @property
    def filename(self):
        return (
            self.module['path'] + '/' + 
            self.module['name']
        )

    def _sorted_funcs(self):
        return sorted(
            self.module['functions'].values(),
            key=lambda f: f['number']
        )
    
    def _block_id(self, func, block):
        return (
            self.module['path'] + '/' + 
            self.module['name'] + '.' + 
            func['name'] + '.' +
            block['name']
        )
