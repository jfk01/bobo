import tables
import os
from os import path
import viset.download
from viset.dataset import SegmentationViset
from viset.util import isimg

class WeizmannHorsesSingleScale():
    URL = 'http://jamie.shotton.org/work/data/WeizmannSingleScale.zip'
    SHA1 = '2d90eedfedea31ebd97294a9268c06fbd4e52332'
    IMGPATH = os.path.join('horses','images')
    MASKPATH = os.path.join('horses','masks')  
    _dbname = 'weizmann_horses_singlescale'
    verbose = True
    
    def export(self, verbose=False):
        # Create empty database
        db = SegmentationViset(self._dbname, mode='w', verbose=verbose)

        # Fetch data necessary to initial construction
        pkgdir = db.cache.get(self.URL, sha1=self.SHA1)        
        imdir = path.join(pkgdir, self.IMGPATH)      
        maskdir = path.join(pkgdir, self.MASKPATH)                      

        # Write images and annotations
        imstream = db.image
        for filename in os.listdir(imdir):
            if isimg(filename):
                imstream.write(self.URL, subpath=path.join(self.IMGPATH, filename))

        # Write labels to database
        idx_image = 0
        annostream = db.annotation.segmentation
        for filename in os.listdir(maskdir):
            if isimg(filename):
                annostream.write('horse', 0, idx_image, maskurl=self.URL, subpath=path.join(self.MASKPATH, filename))                                
                idx_image += 1

        # Cleanup
        db.close()
        return db.abspath()

class WeizmannHorsesMultiScale():
    URL = 'http://jamie.shotton.org/work/data/WeizmannMultiScale.zip'
    SHA1 = '416da2e71f67fdded562e4aabff94227bed48e6b'
    IMGPATH = 'Images'
    MASKPATH = 'Masks'
    _dbname = 'weizmann_horses_multiscale'

    def export(self, verbose=False):
        # Create empty database
        db = SegmentationViset(self._dbname, mode='w', verbose=verbose)

        # CONVENIENCE: don't accidentally clear 2GB on a dumb typo
        db.cache._refetch = False
        
        # Fetch data necessary to initial construction
        pkgdir = db.cache.get(self.URL, sha1=self.SHA1)        
        imdir = path.join(pkgdir, self.IMGPATH)      
        maskdir = path.join(pkgdir, self.MASKPATH)              
                
        # Write images to database
        imstream = db.image
        for filename in os.listdir(imdir):
            if isimg(filename):
                imstream.write(self.URL, subpath=path.join(self.IMGPATH, filename))

        # Write labels to database
        k_mask = 0
        filenames = os.listdir(maskdir)
        annostream = db.annotation.segmentation
        for k in range(0,49):
            annostream.write('horse', 0, k, maskurl=self.URL, subpath=path.join(self.MASKPATH, filenames[k_mask]))
            k_mask += 1
        for k in range(50,99):
			annostream.write('background', 1, k, maskurl=None, subpath=None)
        for k in range(100,149):
            annostream.write('horse', 0, k, maskurl=self.URL, subpath=path.join(self.MASKPATH, filenames[k_mask]))
            k_mask += 1
        for k in range(150,199):
			annostream.write('background', 1, k, maskurl=None, subpath=None)
        for k in range(200,147):
            annostream.write('horse', 0, k, maskurl=self.URL, subpath=path.join(self.MASKPATH, filenames[k_mask]))
            k_mask += 1
        for k in range(248,655):
			annostream.write('background', 1, k, maskurl=None, subpath=None)            

        # FIXME: add bounding boxes
		
        # Cleanup
        db.close()
        return db.abspath()
    


