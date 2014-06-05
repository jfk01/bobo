import os
import csv
from viset.cache import Cache

URL = ('http://www.vision.caltech.edu/Image_Datasets/Caltech256/256_ObjectCategories.tar')
SHA1 = '2195e9a478cf78bd23a1fe51f4dabe1c33744a1c'
VISET = 'caltech256'


def download(outdir=None):
    return Cache(outdir).get(URL, sha1=SHA1, cacheid=VISET)
    
def export(outfile='caltech256.csv', outdir=None, do_json=False):
    # Cache dataset
    pkgdir = download(outdir);

    # Return json or CSV file containing dataset description    
    categorydir = os.path.join(pkgdir, '256_ObjectCategories')          

    # Write to annotation stream
    with open(outfile, 'wb') as csvfile:        
        f = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for (idx_category, category) in enumerate(os.listdir(categorydir)):
            imdir = os.path.join(categorydir, category)        
            for im in os.listdir(imdir):
                f.writerow([os.path.join(categorydir, category, im), category, str(idx_category)]);

    # Return CSV file
    return outfile



    


