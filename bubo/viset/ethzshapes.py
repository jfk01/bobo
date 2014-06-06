import os
import csv
from bubo.cache import Cache
from bubo.util import remkdir, isstring
from bubo.image import ImageDetectionStream
import numpy as np

URL = 'http://www.vision.ee.ethz.ch/datasets/downloads/ethz_shape_classes_v12.tgz'
SHA1 = 'ae9b8fad2d170e098e5126ea9181d0843505a84b'
SUBDIR = 'ETHZShapeClasses-V1.2'
LABELS = ['Applelogos','Bottles','Giraffes','Mugs','Swans']
VISET = 'ethzshapes'

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
    categorydir = LABELS
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
    
