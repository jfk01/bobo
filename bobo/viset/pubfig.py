import os
import csv
from bobo.cache import Cache
from bobo.util import remkdir
from bobo.image import ImageCategoryStream

DEV_IMAGES_URL = 'http://www.cs.columbia.edu/CAVE/databases/pubfig/download/dev_urls.txt'
#DEV_PEOPLE_URL = 'http://www.cs.columbia.edu/CAVE/databases/pubfig/download/dev_people.txt'
#EVAL_PEOPLE_URL = 'http://www.cs.columbia.edu/CAVE/databases/pubfig/download/eval_people.txt'
EVAL_IMAGES_URL = 'http://www.cs.columbia.edu/CAVE/databases/pubfig/download/eval_urls.txt'
VISET = 'pubfig'

DEV_IMAGES_SHA1 = '9eb10c01d46c5d06a8f70b9b8a9ff6b8fe4b0e41';
EVAL_IMAGES_SHA1 = '0fd4cfc464993909c45f9bce1322747c9a9baef9';

cache = Cache(subdir=VISET)

def stream(outdir=None):
    """Return interface objects for this dataset"""
    if outdir is not None:
        cache.setroot(outdir)
    csvfile = os.path.join(cache.root(), '%s.csv' % VISET)            
    if not os.path.isfile(csvfile):
        csvfile = export()
    return ImageCategoryStream(csvfile, cache=cache)

def export(outdir=None):
    """Get metadata and prepare locally cached viset representation"""
    # Update cache
    if outdir is not None:
        cache.setroot(outdir)
    
    # Fetch text files
    txt_dev_images = cache.get(DEV_IMAGES_URL, sha1=DEV_IMAGES_SHA1)
    txt_eval_images = cache.get(EVAL_IMAGES_URL, sha1=EVAL_IMAGES_SHA1)

    # Output file
    outfile = os.path.join(cache.root(), '%s.csv' % VISET)
            
    # Write images and annotations
    with open(outfile, 'wb') as csvfile:            
        f = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)        
        for (k, line) in enumerate(open(txt_dev_images,'r')):
            row = line.decode('utf-8').rstrip().split()
            if row[0] is not '#':
                f.writerow([row[3], '%s_%s' % (row[0], row[1])])

            if (k % 1000) == 0:
                print '[viset.library.pubfig][%d/16000]: exporting "%s"' % (k, row[3])
                
    # Done!
    return outfile

