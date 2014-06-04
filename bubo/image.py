import csv
from bubo.cache import CachedObject, Cache, CacheError
from bubo.show import imshow
from bubo.util import isnumpy, quietprint
import httplib, urllib2

class ImageCategory():
    cachedimage = None
    image = None
    category = None
    cache = None
    
    def __init__(self, image=None, category=None, cache=Cache()):
        if isnumpy(image):
            self.image = image
        elif image is not None:
            self.cachedimage = CachedObject(image, cache)
        self.category = category
        self.cache = cache
        
    def __repr__(self):
        if self.image is not None:
            return str('<viset.image.imcategory: image=(%d,%d), category="%s">' % (self.image.shape[0], self.image.shape[1], self.category))
        else:
            return str('<viset.image.imcategory: uri="%s", category="%s">' % (self.cachedimage.uri, self.category))            
            return self.cachedimage.__repr__()

    def parse(self, row):
        """Parse a row from a viset csv textfile into image and category"""
        rowlist = str(row).split()
        self.category = rowlist[1]
        self.cachedimage = CachedObject(rowlist[0], cache=self.cache)        
        self.image = None
        return self
    
    def load(self):
        """Load images from cache"""
        if self.image is not None:
            return self.image
        elif self.cachedimage is not None:
            try:
                quietprint('[viset.image]: loading cached image "%s"'% self.cachedimage.uri, True);                
                self.image = self.cachedimage.load()
            except (httplib.BadStatusLine, urllib2.URLError, urllib2.HTTPError):
                quietprint('[viset.image][WARNING]: download failed - ignoring image', True);
            except CacheError:
                quietprint('[viset.image][WARNING]: cache error during download - ignoring image', True);                
            except:
                raise
                
            return self.image
        else:
            return None

                
    def show(self):
        if self.load() is not None:
            imshow(self.image)


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

                
class ImageDetection():
    pass


        
class ImageDetectionStream(object):
    pass    

