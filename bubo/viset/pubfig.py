import os
import csv
from bubo.cache import Cache
from bubo.util import remkdir
from bubo.image import ImageCategoryStream

DEV_IMAGES_URL = 'http://www.cs.columbia.edu/CAVE/databases/pubfig/download/dev_urls.txt'
#DEV_PEOPLE_URL = 'http://www.cs.columbia.edu/CAVE/databases/pubfig/download/dev_people.txt'
#EVAL_PEOPLE_URL = 'http://www.cs.columbia.edu/CAVE/databases/pubfig/download/eval_people.txt'
EVAL_IMAGES_URL = 'http://www.cs.columbia.edu/CAVE/databases/pubfig/download/eval_urls.txt'
VISET = 'pubfig'

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
    txt_dev_images = cache.get(DEV_IMAGES_URL)
    txt_eval_images = cache.get(EVAL_IMAGES_URL)

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

