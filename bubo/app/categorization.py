from bubo.parallel import parallelize
import bubo.metric
from bubo.util import Stopwatch

class StreamAlgorithm(object):
    """Base streaming algorithm class"""
    _model = None
    _hyperprms = None
    _name = None
    _parallel = None
    
    @staticmethod
    def preprocess(im):
        IOError('overloaded by plugin')        
        return im

    @staticmethod
    def predict(im, model):
        IOError('overloaded by plugin')

    @staticmethod
    def correct(im, label, model):
        IOError('overloaded by plugin')

        
class Categorization(StreamAlgorithm):
    """Streaming categorization algorithm class"""
    _parallel = None
    
    def __init__(self, plugin, parallel=None):
        self._parallel = parallel
        self.predict = parallelize(plugin.predict, parallel=parallel)
        self.correct = parallelize(plugin.correct, parallel=parallel)            
        self.preprocess = parallelize(plugin.preprocess, parallel=parallel)                        
        self._name = plugin.name
        
    def prediction(self, imstream, outstream=None):
        for im in imstream:
            with Stopwatch() as stopwatch:
                impp = self.preprocess(im)  # parallel
                label = self.predict(impp)  # parallel            
            outstream.write()
            outstream.flush()
        return outstream
            
    def correction(self, trainstream, outstream=None):
        for (im, anno) in trainstream:
            self.correct(self.preprocess(im), anno) 
            if outstream is not None:
                outstream.write()
        return outstream
                
    def prediction_and_correction(self, instream, outstream):
        for (im, anno) in instream:
            if anno is None:
                label = self.predict(self.preprocess(im))
            else:
                self.correct(self.preprocess(im), anno)  
            outstream.write()
        return outstream
        
    def train_and_test(self, trainstream, teststream, outstream=None, model=None):
        for (im, anno) in trainstream(parallel=self._parallel, async=True):
            model = self.correct(self.preprocess(im), anno['category'], model) 
            # separate models for each process?  should we care about combining?
        for (im, anno) in teststream(parallel=self._parallel, async=True):
            with Stopwatch() as stopwatch:
                (label, score) = self.predict(self.preprocess(im), model) 
            outstream.write(label, score, im.url(), stopwatch.elapsed, truelabel=anno['category'])
        outstream.flush()
        return (outstream, model)

    
class CategorizationStorm(Categorization):
    """Exports thrift structures for storm deployment that implement the stream algorithms on spouts for categorization, and tests storm in local mode"""
    pass



def report_categorization(outstream):
    """Return a categorization evaluation result for user display and for bubo.metric.report display"""
    truelabels = outstream.truelabels()
    ap = [bubo.metric.average_precision(outstream.y_true(label), outstream.y_pred(label)) for label in truelabels]
    f1 = [bubo.metric.f1_score(outstream.y_true(label), outstream.y_pred(label)) for label in truelabels]
    pr = [bubo.metric.precision_recall(outstream.y_true(label), outstream.y_pred(label, binary=True)) for label in truelabels]
    confusion = bubo.metric.confusion_matrix(outstream.Y_true(), outstream.Y_pred())
    return (ap, f1, confusion, pr, truelabels)
