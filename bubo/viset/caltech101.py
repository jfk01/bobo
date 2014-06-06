import os
import csv
from bubo.cache import Cache
from bubo.image import ImageCategoryStream

URL = 'http://www.vision.caltech.edu/Image_Datasets/Caltech101/101_ObjectCategories.tar.gz'
SHA1 = 'b8ca4fe15bcd0921dfda882bd6052807e63b4c96'
VISET = 'caltech101'
SUBDIR = '101_ObjectCategories'

cache = Cache(subdir=VISET)

def stream(outdir=None):
    if outdir is not None:
        cache.setroot(outdir)    
    csvfile = os.path.join(cache.root(), '%s.csv' % VISET)            
    if not os.path.isfile(csvfile):
        csvfile = export()
    
    return ImageCategoryStream(csvfile, cache=cache)

def export(outdir=None):
    # Unpack dataset
    if outdir is not None:
        cache.setroot(outdir)
    key = cache.get(URL)
    pkgdir = cache.unpack(key, None, sha1=SHA1, cleanup=False)

    # Output file
    outfile = cache.abspath('%s.csv' % VISET)    
    
    # Return json or CSV file containing dataset description    
    categorydir = os.path.join(cache.root(), SUBDIR)          

    # Write to annotation stream
    with open(outfile, 'wb') as csvfile:        
        f = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for (idx_category, category) in enumerate(os.listdir(categorydir)):
            imdir = os.path.join(categorydir, category)        
            for im in os.listdir(imdir):
                f.writerow([cache.key(os.path.join(categorydir, category, im)), category]);

    # Return CSV file
    return outfile




