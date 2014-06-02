import tables
import os
from os import path
import viset.download
from viset.dataset import CategorizationViset

class ImageNet():
    def export(self, verbose=False):            
        # Create empty database
        db = CategorizationViset(self._dbname, mode='w', verbose=verbose)

        # Fetch textfile for construction
        pkgdir = db.cache.get(self.URL, sha1=self.SHA1)        
        txtfile = path.join(pkgdir,self.TXTFILE)
        
        # Write images and annotations
        imstream = db.image        
        annostream = db.annotation.categorization
        for line in open(txtfile,'r'):
            try:
                (name, url) = line.rstrip().split('\t')
                (synset, suffix) = name.rstrip().split('_')      
                idx_image = imstream.write(url)                             
                annostream.write(str(synset), int(synset[1:]), idx_image)                
            except:
                print '[viset.imagenet]: Warning: Ignoring malformed line "' + line[0:64] + ' ..."'
                
        # Cleanup
        db.close()
        return db.abspath()


class ImageNetFall2011(ImageNet):
  URL = 'http://www.image-net.org/archive/imagenet_fall11_urls.tgz'
  SHA1 = 'f5fd118232b871727fe333778be81df6c6fec372'
  TXTFILE = 'fall11_urls.txt'
  _dbname = 'imagenet_fall2011'

  
