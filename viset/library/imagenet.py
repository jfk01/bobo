import os
import csv
from bubo.cache import Cache
from bubo.util import remkdir, isstring
from bubo.image import ImageCategoryStream
from nltk.corpus import wordnet

URL = 'http://image-net.org/imagenet_data/urls/imagenet_fall11_urls.tgz'
SHA1 = 'f5fd118232b871727fe333778be81df6c6fec372'
TXTFILE = 'fall11_urls.txt'
VISET = 'imagenet_fall2011'


def csvfile(outdir=None):
    return os.path.join(cache(outdir).root(), subdir=VISET, '%s.csv' % VISET)
    
def cache(outdir=None):
    return Cache(outdir, subdir=VISET)
    
def category(wnid):
    pos = wnid[0]
    synset = wordnet._synset_from_pos_and_offset(pos, int(str(wnid[1:]).lstrip('0')))  # assume noun
    return str(synset.lemmas[0].name).replace(" ","_")

def download(csvfile):
    # Initialize cache (if not provided)
    for imcategory in ImageCategoryStream(csvfile, cache=cache()):
        imcategory.show()
        
def export(synset=None, cache=None):
    # Initialize cache (if not provided)
    if cache is None:
        cache = Cache(subdir=VISET)
        
    # Fetch textfile for construction
    txtfile = os.path.join(cache.root(), TXTFILE)
    if not os.path.isfile(txtfile):
        cache.unpack(cache.get(URL), unpackto=None, sha1=SHA1, cleanup=False)                 
    outfile = os.path.join(cache.root(), '%s.csv' % VISET)
            
    # Write images and annotations
    with open(outfile, 'wb') as csvfile:            
        f = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)        
        for (k, line) in enumerate(open(txtfile,'r')):
            try:
                (name, url) = line.rstrip().split('\t')
                (synset, suffix) = name.rstrip().split('_')      
                f.writerow([url, category(synset)])
            except KeyboardInterrupt:
                raise
            except ValueError:
                print '[viset.imagenet]: Warning: Ignoring malformed line "' + line[0:64] + ' ..."'                
            except:
                raise

            if (k % 10000) == 0:
                print '[viset.library.imagenet][%d/14200000]: exporting "%s"' % (k, url)
                
    # Done!
    return outfile

