import numpy as np
import random

name = 'FrequencyDistributedLabels'

def preprocess(im):
    print '[dummy.preprocess]: ' + str(im)
    return im
    
def predict(im, model):
    print '[dummy.predict]: ' + str(im)
    labels = model.keys()
    prob = np.array(model.values(), dtype=np.float32)
    prob = prob / sum(prob)
    label = np.random.choice(labels, size=1, replace=False, p=prob).tolist()[0]
    return (label, random.random())

def correct(im, label, model=None):
    if model is None:
        model = {}
    if label not in model.keys():
        model[label] = 0
    else:            
        model[label] += 1
    print '[dummy.correct]: label = ' + str(label) + ', im = ' + str(im)
    return model

    
