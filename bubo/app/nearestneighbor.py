class Plugin(object):
    name = None
    opt = None
    
    @staticmethod
    def query(X, model, k=1):
        raise IOError('overloaded by plugin')

    @staticmethod
    def update(X, label, model):
        raise IOError('overloaded by plugin')        

    def __call__(self, opt):
        self.opt = opt
        return self
        
class NearestNeighbor(Plugin):
    def __init__(self, plugin, parallel=None):
        self.query = plugin.query
        self.update = plugin.update
        self.name = plugin.name

    def retrieval(self, instream, model=None, outstream=[]):
        """Retrieval task for nearest neighbor queries"""
        for (x, y) in instream:
            model = self.update(x, y, model)
        for (x, y) in instream:
            outstream.append((y, self.query(x, model)))  # mutable parameter
        return (outstream, model)  
    
def eval(self, outstream):
    """Evaluation of a nearest neighbor retrieval task - all output stream results must fit into memory"""
    (y, yhat) = zip(*outstream)
    

    
