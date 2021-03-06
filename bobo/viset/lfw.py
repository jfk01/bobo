import os
import csv
from bobo.cache import Cache
from bobo.util import remkdir, isstring
from bobo.image import ImageCategoryStream

URL = 'http://vis-www.cs.umass.edu/lfw/lfw.tgz'
URL_DEEPFUNNEL = 'http://vis-www.cs.umass.edu/lfw/lfw-deepfunneled.tgz'
URL_FUNNEL = 'http://vis-www.cs.umass.edu/lfw/lfw-funneled.tgz'
URL_LFWA = 'http://www.openu.ac.il/home/hassner/data/lfwa/lfwa.tar.gz'
URL_NAMES = 'http://vis-www.cs.umass.edu/lfw/lfw-names.txt'

SHA1 = 'f5fd118232b871727fe333778be81df6c6fec372'
VISET = 'lfw'
SUBDIR = 'lfw'

cache = Cache(subdir=VISET)


def tinystream():
    csvfile = os.path.join(cache.root(), '%s.csv' % VISET)    
    trainPeople = ['Tom_Cruise','Harrison_Ford']
    imstream = ImageCategoryStream(csvfile, cache=Cache(subdir=VISET))
    trainset = [im for im in imstream if any(substr in im.cachedimage.uri for substr in trainPeople)]
    return trainset
    
def stream(outdir=None):
    if outdir is not None:
        cache.setroot(outdir)
    csvfile = os.path.join(cache.root(), '%s.csv' % VISET)            
    if not os.path.isfile(csvfile):
        csvfile = export(outdir=outdir)        
    return ImageCategoryStream(csvfile, cache=cache)
        
def export(outdir=None):
    # Update cache
    if outdir is not None:
        cache.setroot(outdir)
        
    # Fetch tarfile for construction
    cache.unpack(cache.get(URL, sha1=SHA1), unpackto=None, cleanup=False)
    outfile = os.path.join(cache.root(), '%s.csv' % VISET)
            
    # Write images and annotations
    categorydir = os.path.join(cache.root(), SUBDIR)
    with open(outfile, 'wb') as csvfile:            
        f = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)        
        for (idx_category, category) in enumerate(os.listdir(categorydir)):
            if os.path.isdir(os.path.join(categorydir, category)):
                imdir = os.path.join(categorydir, category)        
                for im in os.listdir(imdir):
                    f.writerow([cache.key(os.path.join(categorydir, category, im)), category]);

    # Done!
    return outfile

