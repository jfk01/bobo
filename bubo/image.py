import csv
from bubo.cache import CachedObject, Cache, CacheError
from bubo.show import imshow, imbbox
from bubo.util import isnumpy, quietprint, isstring
import httplib, urllib2


class Image():
    cachedimage = None
    image = None
    cache = None
    
    def __init__(self, image=None, cache=Cache()):
        if isnumpy(image):
            self.image = image
        elif image is not None:
            self.cachedimage = CachedObject(image, cache)
        self.cache = cache
        
    def __repr__(self):
        if self.image is not None:
            return str('<bubo.image: image=(%d,%d)>' % (self.image.shape[0], self.image.shape[1]))
        else:
            return str('<bubo.image: uri="%s">' % (self.cachedimage.uri))            

    def parse(self, row):
        """Parse a row from a viset csv textfile into image"""
        self.cachedimage = CachedObject(row, cache=self.cache)        
        self.image = None
        return self
    
    def load(self):
        """Load images from cache"""
        if self.image is not None:
            return self.image
        elif self.cachedimage is not None:
            try:
                quietprint('[bubo.image]: loading "%s"'% self.cachedimage.uri, True);                
                self.image = self.cachedimage.load()
            except (httplib.BadStatusLine, urllib2.URLError, urllib2.HTTPError):
                quietprint('[bubo.image][WARNING]: download failed - ignoring image', True);
            except CacheError:
                quietprint('[bubo.image][WARNING]: cache error during download - ignoring image', True);                
            except IOError:
                quietprint('[bubo.image][WARNING]: IO error during download - ignoring image', True);                
            except:
                #raise
                quietprint('[bubo.image][WARNING]: error during download - ignoring image', True);                
                pass
                
            return self.image
        else:
            return None

    def show(self):
        if self.load() is not None:
            imshow(self.image)

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
            return str('<bubo.image.imcategory: image=(%d,%d), category="%s">' % (self.image.shape[0], self.image.shape[1], self.category))
        else:
            return str('<bubo.image.imcategory: uri="%s", category="%s">' % (self.cachedimage.uri, self.category))            

    def parse(self, row):
        """Parse a row from a viset csv textfile into image and category"""
        rowlist = row.encode('utf-8').split()
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
                quietprint('[bubo.image]: loading "%s"'% self.cachedimage.uri, True);                
                self.image = self.cachedimage.load()
            except (httplib.BadStatusLine, urllib2.URLError, urllib2.HTTPError):
                quietprint('[bubo.image][WARNING]: download failed - ignoring image', True);
            except CacheError:
                quietprint('[bubo.image][WARNING]: cache error during download - ignoring image', True);                
            except IOError:
                quietprint('[bubo.image][WARNING]: IO error during download - ignoring image', True);                
            except:
                raise
                
            return self.image
        else:
            return None

    def iscategory(self, category):
        return (self.category.lower() == category.lower())
                
    def show(self):
        if self.load() is not None:
            imshow(self.image)


class ImageCategoryStream(object):
    """A stream of labeled imagery"""
    _csvfile = None
    _cache = None
    reader = None
    
    def __init__(self, csvfile, cache=Cache()):        
        self._csvfile = csvfile
        self._cache = cache

    def __iter__(self):
        self.reader = csv.reader(open(self._csvfile, 'rb'), delimiter=' ', quotechar='|')  # reopen
        return self

    def __getitem__(self, item):
        if isstring(item):
            # assume that item is a row from a viset csv file
            return ImageCategory(cache=self._cache).parse(item)
        else:
            # Inefficient method for random stream access
            print type(item)
            f = open(self._csvfile, 'r')
            for i in range(item):
                line = f.readline()
                if len(line) == 0:
                    raise IndexError('Invalid index "%d"' % item)  # end of file
            f.close()
            row = line.split()
            return (ImageCategory(row[0], category=row[1], cache=self._cache))        

    def next(self):
        row = self.reader.next()
        return (ImageCategory(row[0], category=row[1], cache=self._cache))

                
class ImageDetection():
    cachedimage = None
    image = None
    category = None
    cache = None
    xmin = None
    xmax = None
    ymin = None
    ymax = None
    
    def __init__(self, image=None, category=None, xmin=None, xmax=None, ymin=None, ymax=None, cache=Cache()):
        if isnumpy(image):
            self.image = image
        elif image is not None:
            self.cachedimage = CachedObject(image, cache)
        self.category = category
        self.cache = cache
        self.xmin = float(xmin)
        self.xmax = float(xmax)
        self.ymin = float(ymin)
        self.ymax = float(ymax)
        
    def __repr__(self):
        if self.image is not None:
            return str('<bubo.image.imdetection: image=(%d,%d), category="%s, bbox=(%d,%d,%d,%d)">' % (self.image.shape[0], self.image.shape[1], self.category, self.xmin,self.ymin,self.xmax,self.ymax))
        else:
            return str('<bubo.image.imdetection: uri="%s", category="%s", bbox=(%d,%d,%d,%d)">' % (self.image.shape[0], self.image.shape[1], self.category, self.xmin,self.ymin,self.xmax,self.ymax))

    def parse(self, row):
        """Parse a row from a viset csv textfile into image and category"""
        rowlist = row.encode('utf-8').split()
        self.category = rowlist[1]
        self.cachedimage = CachedObject(rowlist[0], cache=self.cache)        
        self.image = None
        self.xmin = float(rowlist[2])
        self.ymin = float(rowlist[3])
        self.xmax = float(rowlist[4])
        self.ymax = float(rowlist[5])
        return self
    
    def load(self):
        """Load images from cache"""
        if self.image is not None:
            return self.image
        elif self.cachedimage is not None:
            try:
                quietprint('[bubo.image]: loading "%s"'% self.cachedimage.uri, True);                
                self.image = self.cachedimage.load()
            except (httplib.BadStatusLine, urllib2.URLError, urllib2.HTTPError):
                quietprint('[bubo.image][WARNING]: download failed - ignoring image', True);
            except CacheError:
                quietprint('[bubo.image][WARNING]: cache error during download - ignoring image', True);                
            except IOError:
                quietprint('[bubo.image][WARNING]: IO error during download - ignoring image', True);                
            except:
                raise
                
            return self.image
        else:
            return None

    def iscategory(self, category):
        return (self.category.lower() == category.lower())
                
    def show(self):
        if self.load() is not None:
            imbbox(self.image, self.xmin, self.xmax, self.ymin, self.ymax, bboxcaption=self.category)         

        
class ImageDetectionStream(object):
    """A stream of labeled detections"""
    _csvfile = None
    _cache = None
    reader = None
    
    def __init__(self, csvfile, cache=Cache()):        
        self._csvfile = csvfile
        self._cache = cache

    def __iter__(self):
        self.reader = csv.reader(open(self._csvfile, 'rb'), delimiter=' ', quotechar='|')  # reopen
        return self

    def __getitem__(self, item):
        if isstring(item):
            # assume that item is a row from a viset csv file
            return ImageDetection(cache=self._cache).parse(item)
        else:
            # Inefficient method for random stream access
            print type(item)
            f = open(self._csvfile, 'r')
            for i in range(item):
                line = f.readline()
                if len(line) == 0:
                    raise IndexError('Invalid index "%d"' % item)  # end of file
            f.close()
            row = line.split()
            return (ImageDetection(row[0], category=row[1], xmin=row[2], ymin=row[3], xmax=row[4], ymax=row[5], cache=self._cache))        

    def next(self):
        row = self.reader.next()
        return (ImageDetection(row[0], category=row[1], xmin=row[2], ymin=row[3], xmax=row[4], ymax=row[5], cache=self._cache))                


