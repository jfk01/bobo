import csv
from viset.cache import CachedObject, Cache
from viset.show import imshow
from viset.util import isnumpy, quietprint


class ImageCategory():
    cachedimage = None
    image = None
    category = None
    
    def __init__(self, image, category=None, cache=Cache()):
        if isnumpy(image):
            self.image = image
        else:
            self.cachedimage = CachedObject(image, cache)
        self.category = category

    def __repr__(self):
        if self.image is not None:
            return str('<viset.image.imcategory: image=(%d,%d), category="%s">' % (self.image.shape[0], self.image.shape[1], self.category))
        else:
            return str('<viset.image.imcategory: uri="%s", category="%s">' % (self.cachedimage.uri, self.category))            
            return self.cachedimage.__repr__()
        
    def load(self):
        if self.cachedimage is not None:
            self.image = self.cachedimage.load()
        return self.image
            
    def show(self):
        try:
            imshow(self.load(), title=self.category)
        except KeyboardInterrupt:
            raise
        except:
            quietprint('[viset.image][WARNING]: download failed', True);

    
class ImageDetection():
    pass


class ImageCategoryStream(object):
    """A stream of labeled imagery"""
    _csvfile = None
    _cache = None
    
    def __init__(self, csvfile, cache=Cache()):        
        self._csvfile = csvfile
        self._cache = cache
        self.reader = csv.reader(open(self._csvfile, 'rb'), delimiter=' ', quotechar='|')

    def __iter__(self):
        return self

    def next(self):
        row = self.reader.next()
        return (ImageCategory(row[0], category=row[1], cache=self._cache))

    def parse(self, row):
        return ImageCategory(row[0], category=row[1], cache=self._cache)

        
class DetectionStream(object):
    pass    

