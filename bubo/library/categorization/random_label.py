import random

name = 'UniformRandomLabels'
    
def preprocess(im):
    print '[dummy.preprocess]: passthrough'
    return im
    
def predict(im, model):
    labels = model.keys()
    label = (labels[random.randint(0,len(labels)-1)], random.random())
    print '[dummy.predict]: "%s" ' % str(label)
    return (label, random.random())
    
def correct(im, label, model=None):
    if model is None:
        model = {}
    if label not in model.keys():
        model[label] = 0
    else:            
        model[label] += 1
    print '[dummy.correct]: label = "%s" ' % str(label)
    return model
