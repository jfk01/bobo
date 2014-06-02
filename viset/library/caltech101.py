import os
import csv
from viset.cache import Cache

URL = ('http://www.vision.caltech.edu/Image_Datasets/Caltech101/101_ObjectCategories.tar.gz')
SHA1 = 'b8ca4fe15bcd0921dfda882bd6052807e63b4c96'
VISET = 'caltech101'

def download(outdir=None):
    return Cache(outdir).get(URL, sha1=SHA1, cacheid=VISET)
    
def export(outfile='caltech101.csv', outdir=None, do_json=False):
    # Cache dataset
    pkgdir = download(outdir);

    # Return json or CSV file containing dataset description    
    categorydir = os.path.join(pkgdir, '101_ObjectCategories')          

    # Write to annotation stream
    with open(outfile, 'wb') as csvfile:        
        f = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for (idx_category, category) in enumerate(os.listdir(categorydir)):
            imdir = os.path.join(categorydir, category)        
            for im in os.listdir(imdir):
                f.writerow([os.path.join(categorydir, category, im), category, str(idx_category)]);

    # Return CSV file
    return outfile




