from bobo.viset import lfw

lfw.URL = 'http://vis-www.cs.umass.edu/lfw/lfw-funneled.tgz'
lfw.SHA1 = None
lfw.SUBDIR = 'lfw_funneled'
lfw.VISET = 'lfw'

def stream(outdir=None):
    return lfw.stream(outdir)
        
def export(outdir=None):
    return lfw.export(outdir)


