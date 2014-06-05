import os
from viset.dataset import ImageViset
from viset.util import quietprint, isimg, filepath2url

class ImageDir(object):
    def export(self, dbname, imdir, verbose=False):            
        # Inputs
        if not os.path.isdir(imdir):
            raise IOError('input path is not directory')
        
        # Create empty database
        db = ImageViset(dbname, mode='w', verbose=verbose)
        
        # Write images in directory order
        imstream = db.image        
        for filename in os.listdir(imdir):
            filepath = os.path.join(imdir, filename)
            if isimg(filepath):
                quietprint('[viset.library.imagedir]: writing "%s"' % filepath, verbose)
                imstream.write(url=filepath)
                
        # Cleanup
        db.close()
        return db.abspath()

  
