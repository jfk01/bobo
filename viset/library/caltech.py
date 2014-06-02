import os
from os import path
from viset.dataset import CategorizationViset
from viset.util import isimg

class Caltech():
    def export(self, verbose=False):
        # Create empty database
        db = CategorizationViset(self._dbname, mode='w', verbose=verbose)

        # Fetch data necessary to initial construction
        #db.cache._refetch = False
        pkgdir = db.cache.get(self.URL, sha1=self.SHA1)
        categorydir = path.join(pkgdir, self.PATH)          
                
        # Write to annotation stream
        imstream = db.image
        annostream = db.annotation.categorization
        for (idx_category, category) in enumerate(os.listdir(categorydir)):
            imdir = path.join(categorydir, category)        
            for im in os.listdir(imdir):
                idx_image = imstream.write(self.URL, subpath=path.join(self.PATH, category, im))
                annostream.write(category, idx_category, idx_image)
        
        # Cleanup
        db.close()
        return db.abspath()
    
