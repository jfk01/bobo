import os
import csv
from bubo.cache import Cache
import bubo.viset.caltech101

URL = ('http://www.vision.caltech.edu/Image_Datasets/Caltech256/256_ObjectCategories.tar')
SHA1 = '2195e9a478cf78bd23a1fe51f4dabe1c33744a1c'
VISET = 'caltech256'
SUBDIR = '256_ObjectCategories'

def stream(csvfile=None, outdir=None):
    bubo.viset.caltech101.cache = Cache(cacheroot=outdir, subdir=VISET)
    bubo.viset.caltech101.URL = URL
    bubo.viset.caltech101.SHA1 = SHA1
    bubo.viset.caltech101.VISET = VISET
    bubo.viset.caltech101.SUBDIR = SUBDIR    
    return bubo.viset.caltech101.stream(csvfile, outdir)

def export(outdir=None):
    bubo.viset.caltech101.cache = Cache(cacheroot=outdir, subdir=VISET)    
    bubo.viset.caltech101.URL = URL
    bubo.viset.caltech101.SHA1 = SHA1
    bubo.viset.caltech101.VISET = VISET
    bubo.viset.caltech101.SUBDIR = SUBDIR        
    return bubo.viset.caltech101.export(outdir)    

    


