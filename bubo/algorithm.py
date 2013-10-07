from bubo.parallel import vectorize


#pretrain = vectorize(algorithm.preprocess)
#train = vectorize(algorithm.correct)
#test = vectorize(algorithm.predict)     

class StreamAlgorithm(object):
    """Base streaming algorithm class"""
    _model = None
    _hyperprms = None
    _name = None
    _parallel = None
    
    def __init__(self):
        pass

    def preprocess(self, im):
        return im
    
    def predict(self, im):
        IOError('overloaded by subclass')

    def correct(self, im, label):
        IOError('overloaded by subclass')

def test_vectorize(a,b,c=1):
    print 'a=' + str(a)
    print 'b=' + str(b)    
    print 'c=' + str(c)    
    return a+b+c

