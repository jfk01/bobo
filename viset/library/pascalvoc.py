import tables
import os
from os import path
import viset.download
from viset.dataset import Viset, CategorizationDetectionSegmentationViset


class PascalVOC():
    def export(self, verbose=False):
        # Create empty database
        db = CategorizationDetectionSegmentationViset(self._dbname, mode='w', verbose=verbose)

        # CONVENIENCE: don't accidentally clear 2GB on a dumb typo
        db.cache._refetch = False
        
        # Fetch data necessary to initial construction
        pkgdir = db.cache.get(self.URL, sha1=self.SHA1)
        imsetdir = path.join(pkgdir, self.IMSETDIR)                              
        
        # Write images to database
        imstream = db.image
        for line in open(path.join(imsetdir,'trainval.txt'),'r'):        
            im = line.strip() + '.jpg'
            imstream.write(url=self.URL, subpath=path.join(self.IMDIR, im))

        # Write annotations to database
        annostream = db.annotation.categorization        
        for (idx_category, imset) in enumerate(os.listdir(imsetdir)):
            (filebase,ext) = path.splitext(path.basename(imset))
            try:
                (category, set) = filebase.split('_')            
            except:
                continue
            if set == 'trainval':
                for (idx_image, line) in enumerate(open(path.join(imsetdir, imset),'r')):
                    (im, label) = line.strip().split()
                    if int(label) == 1:
                        annostream.write(category, idx_category, idx_image)  

        # Detection annotations
        #tree = ET.parse(xmlfile)
        #root = tree.getroot()
        
        # Cleanup
        db.close()
        return db.abspath()

class PascalVOC2012(PascalVOC):
  URL = 'http://pascallin.ecs.soton.ac.uk/challenges/VOC/voc2012/VOCtrainval_11-May-2012.tar'
  SHA1 = None
  IMDIR = 'VOCdevkit/VOC2012/JPEGImages'
  IMSETDIR = 'VOCdevkit/VOC2012/ImageSets/Main'
  _dbname = 'pascalvoc_2012'
  
