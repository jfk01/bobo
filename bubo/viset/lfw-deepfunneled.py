from bubo.cache import Cache
from bubo.viset import lfw

lfw.URL = 'http://vis-www.cs.umass.edu/lfw/lfw-deepfunneled.tgz'
lfw.SHA1 = None
lfw.SUBDIR = 'lfw-deepfunneled'
lfw.VISET = 'lfw'

def stream(csvfile=None, outdir=None):
    return lfw.stream(csvfile, outdir)
        
def export(outdir=None):
    return lfw.export(csvfile, outdir)


