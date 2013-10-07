from bubo.app.categorization import CategorizationStream
import numpy as np
import random

class UniformRandomLabels(CategorizationStream):
    _name = 'UniformRandomLabels'
    _model = {}
    
    def preprocess(self, im):
        print '[dummy.preprocess]: ' + str(im)
        return im
    
    def predict(self, im):
        print '[dummy.predict]: ' + str(im)
        labels = self._model.keys()
        return (labels[random.randint(0,len(labels)-1)], random.random())
    
    def correct(self, im, label):
        if label not in self._model.keys():
            self._model[label] = 0
        else:            
            self._model[label] += 1
        print '[dummy.correct]: label = ' + str(label) + ', im = ' + str(im)


class FrequencyDistributedLabels(UniformRandomLabels):
    _name = 'FrequencyDistributedLabels'
    
    def predict(self, im):
        print '[dummy.predict]: ' + str(im)
        labels = self._model.keys()
        prob = np.array(self._model.values(), dtype=np.float32)
        prob = prob / sum(prob)
        label = np.random.choice(labels, size=1, replace=False, p=prob).tolist()[0]
        return (label, random.random())
    



    
