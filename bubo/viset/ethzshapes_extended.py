from bubo.cache import Cache
from bubo.viset import ethzshapes

ethzshapes.URL = 'http://www.vision.ee.ethz.ch/datasets/downloads/extended_ethz_shapes.tgz'
ethzshapes.SHA1 = None
ethzshapes.SUBDIR = 'extended_ethz_shapes'
ethzshapes.LABELS = ['apple','bottle','giraffe','hat','mug','starfish','swan']
ethzshapes.VISET = 'ethzshapes'

cache = Cache(subdir=ethzshapes.VISET)

def stream(outdir=None):
    return ethzshapes.stream(outdir)

def export(outdir=None):
    return ethzshapes.export(outdir)

