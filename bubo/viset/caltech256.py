import os
from bubo.viset import caltech101
from bubo.cache import Cache

caltech101.URL = ('http://www.vision.caltech.edu/Image_Datasets/Caltech256/256_ObjectCategories.tar')
caltech101.SHA1 = '2195e9a478cf78bd23a1fe51f4dabe1c33744a1c'
caltech101.VISET = 'caltech256'
caltech101.SUBDIR = '256_ObjectCategories'
caltech101.cache = Cache(None, subdir=caltech101.VISET)

print caltech101.cache.root()

def stream(outdir=None):
    return caltech101.stream(outdir)

def export(outdir=None):
    return caltech101.export(outdir)    

    


