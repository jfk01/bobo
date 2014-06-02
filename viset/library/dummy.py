import tables
import os
from os import path
import viset.download
from viset.dataset import CategorizationViset

class Dummy():
    _dbname = 'dummy'
    URL = ['http://farm4.staticflickr.com/3659/3350646105_e20dee4c5e.jpg',
           'http://farm1.staticflickr.com/199/487029330_3cbe39cdd7.jpg',
           'http://farm6.staticflickr.com/5146/5687458009_1d8cb1efbc.jpg',
           'http://farm3.staticflickr.com/2493/3826383001_8e78085668.jpg',
           'http://farm2.staticflickr.com/1084/942181643_817e498d36.jpg']
    
    def export(self, verbose=False):            
        # Create empty database
        db = CategorizationViset(self._dbname, mode='w', verbose=verbose)

        # Write annotations and images
        imstream = db.image        
        annostream = db.annotation.categorization        
        for k in range(5):
            idx_image = imstream.write(url=self.URL[k]) 
            annostream.write('owl', k, idx_image)                

        # Cleanup
        db.close()
        return db.abspath()


  
