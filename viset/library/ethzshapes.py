import tables
import os
from os import path
import viset.download
from viset.dataset import DetectionViset
import numpy as np

class ETHZShapes():      
    def export(self, verbose=False):
        # Create empty database
        db = DetectionViset(self._dbname, mode='w', verbose=verbose)
        
        # Fetch data necessary to initial construction
        pkgdir = db.cache.get(self.URL, sha1=self.SHA1)
        categorydir = self.LABELS
                
        # Write dataset
        imstream = db.image
        annostream = db.annotation.detection
        for (idx_category, category) in enumerate(categorydir):
            imdir = path.join(pkgdir, self.PATH, category)        
            for filename in os.listdir(imdir):
                if filename.endswith(".jpg") and not filename.startswith('.'):
                    # Write image
                    idx_image = imstream.write(url=self.URL, subpath=path.join(self.PATH, category, filename))

                    # Write detections
                    gtfile = path.join(pkgdir, self.PATH, category, os.path.splitext(path.basename(filename))[0] + '_' + category.lower()+'.groundtruth')
                    if not os.path.isfile(gtfile):
                        gtfile = path.join(pkgdir, self.PATH, category, os.path.splitext(path.basename(filename))[0] + '_' + category.lower()+'s.groundtruth') # plural hack
                    for line in open(gtfile,'r'):
                        if line.strip() == '':
                            continue
                        (xmin,ymin,xmax,ymax) = line.strip().split()
                        annostream.write(category, idx_category, idx_image, np.float32(xmin), np.float32(xmax), np.float32(ymin), np.float32(ymax))
                    
        # Cleanup
        db.close()
        return db.abspath()
    
class ETHZShapeClasses(ETHZShapes):
  URL = 'http://www.vision.ee.ethz.ch/datasets/downloads/ethz_shape_classes_v12.tgz'
  SHA1 = 'ae9b8fad2d170e098e5126ea9181d0843505a84b'
  PATH = 'ETHZShapeClasses-V1.2'
  LABELS = ['Applelogos','Bottles','Giraffes','Mugs','Swans']
  _dbname = 'ethzshapes'
  
class ETHZExtendedShapeClasses(ETHZShapes):
  URL = 'http://www.vision.ee.ethz.ch/datasets/downloads/extended_ethz_shapes.tgz'
  SHA1 = None
  PATH = 'extended_ethz_shapes'
  LABELS = ['apple','bottle','giraffe','hat','mug','starfish','swan']
  _dbname = 'ethzshapes_extended'

