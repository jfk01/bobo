from bubo.algorithm import StreamAlgorithm
from bubo.parallel import vectorize
import bubo.metric
from bubo.util import Stopwatch

class CategorizationStream(StreamAlgorithm):
    """Streaming categorization algorithm class"""
    _parallel = None
    
    def __init__(self, parallel=False):
        self._parallel = parallel
        if parallel:
            self.predict = vectorize(self.predict)
            self.correct = vectorize(self.correct)            
            self.preprocess = vectorize(self.preprocess)                        
        
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
        
    def train_and_test(self, trainstream, teststream, outstream=None):
        for (im, anno) in trainstream(async=True):
            self.correct(self.preprocess(im), anno['category']) 
        for (im, anno) in teststream(async=True):
            with Stopwatch() as stopwatch:
                (label, score) = self.predict(self.preprocess(im)) 
            outstream.write(label, score, stopwatch.elapsed, im.url(), truelabel=anno['category'])
        outstream.flush()
        return outstream

class CategorizationStorm(CategorizationStream):
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
