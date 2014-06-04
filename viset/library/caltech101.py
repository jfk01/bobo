import os
import csv
from bubo.cache import Cache

URL = 'http://www.vision.caltech.edu/Image_Datasets/Caltech101/101_ObjectCategories.tar.gz'
SHA1 = 'b8ca4fe15bcd0921dfda882bd6052807e63b4c96'
VISET = 'caltech101'

def cache(outdir=None):
    return Cache(outdir, subdir=VISET)

def download(outdir=None):
    return Cache(outdir).get(URL, sha1=SHA1, cacheid=VISET)
    
def export(outfile=None, outdir=None, do_json=False):
    # Unpack dataset
    cache = Cache(outdir, subdir=VISET)
    key = cache.get(URL)
    pkgdir = cache.unpack(key, None, sha1=SHA1, cleanup=False)

    # Output file
    if outfile is None:
        outfile = cache.abspath('%s.csv' % VISET)    
    
    # Return json or CSV file containing dataset description    
    categorydir = os.path.join(cache.root(), '101_ObjectCategories')          

    # Write to annotation stream
    with open(outfile, 'wb') as csvfile:        
        f = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for (idx_category, category) in enumerate(os.listdir(categorydir)):
            imdir = os.path.join(categorydir, category)        
            for im in os.listdir(imdir):
                f.writerow([cache.key(os.path.join(categorydir, category, im)), category]);

    # Return CSV file
    return outfile




