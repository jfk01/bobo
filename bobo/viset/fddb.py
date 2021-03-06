import os
import csv
from bobo.cache import Cache
from bobo.util import remkdir, isstring
from bobo.image import ImageDetectionStream

URL = 'http://tamaraberg.com/faceDataset/originalPics.tar.gz'
URL_ANNO = 'http://vis-www.cs.umass.edu/fddb/FDDB-folds.tgz'
SHA1 = None
SUBDIR = 'ETHZShapeClasses-V1.2'
VISET = 'fddb'

cache = Cache(subdir=VISET)

def stream(csvfile=None, outdir=None):
    if csvfile is None:
        csvfile = os.path.join(cache.root(), '%s.csv' % VISET)            
    if outdir is not None:
        cache.setroot(outdir)
    #if not os.path.isfile(csvfile):
    csvfile = export()        
    return ImageDetectionStream(csvfile, cache=cache)

def export(outdir=None):
    # Update cache
    if outdir is not None:
        cache.setroot(outdir)
        
    # Fetch data necessary to initial construction
    pkgdir = cache.unpack(cache.get(URL), sha1=SHA1)
    annodir = cache.unpack(cache.get(URL_ANNO), sha1=SHA1)    
    outfile = os.path.join(cache.root(), '%s.csv' % VISET)
                    
    # Write dataset
    with open(outfile, 'wb') as csvfile:
        f = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)         
        for (idx_category, category) in enumerate(categorydir):
            imdir = os.path.join(pkgdir, SUBDIR, category)        
            for filename in os.listdir(imdir):
                if filename.endswith(".jpg") and not filename.startswith('.'):
                    # Write image
                    im = os.path.join(SUBDIR, category, filename)

                    # Write detections
                    gtfile = os.path.join(pkgdir, SUBDIR, category, os.path.splitext(os.path.basename(filename))[0] + '_' + category.lower()+'.groundtruth')
                    if not os.path.isfile(gtfile):
                        gtfile = os.path.join(pkgdir, SUBDIR, category, os.path.splitext(os.path.basename(filename))[0] + '_' + category.lower()+'s.groundtruth') # plural hack
                    for line in open(gtfile,'r'):
                        if line.strip() == '':
                            continue
                        (xmin,ymin,xmax,ymax) = line.strip().split()
                        f.writerow([im, category, xmin, ymin, xmax, ymax]);
        
    return outfile
    
