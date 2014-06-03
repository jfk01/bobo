import os
import viset.download
import viset.cache
from viset.stream import Recognition
import csv
from viset.show import imshow

URL = 'http://image-net.org/imagenet_data/urls/imagenet_fall11_urls.tgz'
SHA1 = 'f5fd118232b871727fe333778be81df6c6fec372'
TXTFILE = 'fall11_urls.txt'
VISET = 'imagenet_fall2011'

def download(outdir=None, csvfile=None):
    if csvfile is None:
        csvfile = export(csvfile, outdir)
    for (idx, (im, annotation)) in enumerate(Recognition(csvfile)):
        filename = os.path.join(VISET, 'im_%09d.jpg' % idx)
        print filename
        #imshow(im.get(cacheid=filename))
        
def export(outfile=None, outdir=None):
    # Fetch textfile for construction
    if outdir is None:
        outdir = os.path.fullfile(viset.cache.Cache().root(), VISET)
    cache = viset.cache.Cache(outdir);
    if cache.iscached(URL) is False:
        viset.download.download_and_extract(URL, outdir, sha1=SHA1)
    txtfile = os.path.join(cache.root(), TXTFILE)
        
    # Write images and annotations
    if outfile is None:
        outfile = os.path.join(cache.root(), 'imagenet_fall11.csv')
    with open(outfile, 'wb') as csvfile:            
        f = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)        
        for (k, line) in enumerate(open(txtfile,'r')):
            try:
                (name, url) = line.rstrip().split('\t')
                (synset, suffix) = name.rstrip().split('_')      
                f.writerow([url, str(synset)])
            except:
                print '[viset.imagenet]: Warning: Ignoring malformed line "' + line[0:64] + ' ..."'

            if (k % 10000) == 0:
                print '[viset.library.imagenet][%d]: exporting "%s"' % (k, url)
                
    # Done!
    return outfile

