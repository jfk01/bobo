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

def category(wnid):
    pos = wnid[0]
    synset = wordnet._synset_from_pos_and_offset(pos, int(str(wnid[1:]).lstrip('0')))  # assume noun
    return str(synset.lemmas[0].name).replace(" ","_")

def stream(indir=None, outdir=None):
    cache = Cache(subdir=VISET)
    if outdir is not None:
        cache.setroot(outdir)
    if indir is not None:
        csvfile = os.path.join(indir, '%s.csv' % VISET)                    
    else:
        csvfile = os.path.join(cache.root(), '%s.csv' % VISET)            
    if not os.path.isfile(csvfile):
        csvfile = export()        
    return ImageCategoryStream(csvfile, cache=cache)
        
def export(outdir=None):
    # Update cache
    cache = Cache(subdir=VISET)   # non-global cache!
    if outdir is not None:
        cache.setroot(outdir)

    # Fetch textfile for construction
    txtfile = os.path.join(cache.root(), TXTFILE)
    if not os.path.isfile(txtfile):
        cache.unpack(cache.get(URL), unpackto=None, sha1=SHA1, cleanup=False)                 
    outfile = os.path.join(cache.root(), '%s.csv' % VISET)
            
    # Write images and annotations
    if not os.path.isfile(outfile):
        with open(outfile, 'wb') as csvfile:            
            f = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)        
            for (k, line) in enumerate(open(txtfile,'r')):
                try:
                    (name, url) = line.decode('utf-8').rstrip().split('\t')
                    (wnid, suffix) = name.decode('utf-8').rstrip().split('_')      
                    f.writerow([url.encode('utf-8'), wnid.encode('utf-8')])
                except KeyboardInterrupt:
                    raise
                except ValueError:
                    print '[viset.imagenet]: Warning: Ignoring malformed line "' + line[0:64] + ' ..."'                
                except:
                    raise

                if (k % 10000) == 0:
                    print '[bubo.viset.imagenet][%d/14200000]: exporting "%s"' % (k, url.encode('utf-8'))
    else:
        print '[bubo.viset.imagenet]: returning cached viset file "%s"' % (outfile)        

    # Done!
    return outfile

