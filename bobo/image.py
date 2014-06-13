import csv, os
from bobo.cache import CachedObject, Cache, CacheError
from bobo.show import imshow, imbbox
from bobo.util import isnumpy, quietprint, isstring, tempcsv
import httplib, urllib2


def rdd(obj):
    """sc.parallelize on native datatype to convert list into parallelizable construct"""
    return sc.parallelize(obj)
    

def export(objlist, outfile=None):
    if outfile is None:
        outfile = tempcsv()
    with open(outfile, 'wb') as csvobj:
        f = csv.writer(csvobj, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for im in objlist:
            f.writerow(im.export());                                                    
    return outfile
    

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
            return str('<bobo.image: image=(%d,%d)>' % (self.image.shape[0], self.image.shape[1]))
        else:
            return str('<bobo.image: uri="%s">' % (self.cachedimage.uri))            

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
                quietprint('[bobo.image]: loading "%s"'% self.cachedimage.uri, True);                
                self.image = self.cachedimage.load()
            except (httplib.BadStatusLine, urllib2.URLError, urllib2.HTTPError):
                quietprint('[bobo.image][WARNING]: download failed - ignoring image', True);
            except CacheError:
                quietprint('[bobo.image][WARNING]: cache error during download - ignoring image', True);                
            except IOError:
                quietprint('[bobo.image][WARNING]: IO error during download - ignoring image', True);                
            except:
                #raise
                quietprint('[bobo.image][WARNING]: error during download - ignoring image', True);                
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
            return str('<bobo.image.imcategory: image=(%d,%d), category="%s">' % (self.image.shape[0], self.image.shape[1], self.category))
        else:
            return str('<bobo.image.imcategory: uri="%s", category="%s">' % (self.cachedimage.uri, self.category))            

    def __eq__(self, other):
        return self.category.lower() == other.category.lower()

    def __ne__(self, other):
        return self.category.lower() != other.category.lower()

    
    def __hash__(self):
        return hash(self.category.lower())
                
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
                quietprint('[bobo.image]: loading "%s"'% self.cachedimage.uri, True);                
                self.image = self.cachedimage.load()
                if self.cachedimage.size() < 10000:
                    quietprint('[bobo.image][WARNING]: invalid download size - ignoring image', True);                                    
                    os.remove(self.cachedimage.filename())
                    return None
            except (httplib.BadStatusLine, urllib2.URLError, urllib2.HTTPError):
                quietprint('[bobo.image][WARNING]: download failed - ignoring image', True);
                self.cachedimage.discard()                
            except CacheError:
                quietprint('[bobo.image][WARNING]: cache error during download - ignoring image', True);
                self.cachedimage.discard()                
            except IOError:
                quietprint('[bobo.image][WARNING]: IO error during download - ignoring image', True);
                self.cachedimage.discard()                
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

    def export(self):
        """List suitable for export"""
        return [os.path.join(self.cache.root(), self.cachedimage.uri), self.category]

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

    def rdd(self):
        """Return a spark resilient distributed dataset for this image stream"""
        pass

    
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
            return str('<bobo.image.imdetection: image=(%d,%d), category="%s, bbox=(%d,%d,%d,%d)">' % (self.image.shape[0], self.image.shape[1], self.category, self.xmin,self.ymin,self.xmax,self.ymax))
        else:
            return str('<bobo.image.imdetection: uri="%s", category="%s", bbox=(%d,%d,%d,%d)">' % (self.image.shape[0], self.image.shape[1], self.category, self.xmin,self.ymin,self.xmax,self.ymax))

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
                quietprint('[bobo.image]: loading "%s"'% self.cachedimage.uri, True);                
                self.image = self.cachedimage.load()
            except (httplib.BadStatusLine, urllib2.URLError, urllib2.HTTPError):
                quietprint('[bobo.image][WARNING]: download failed - ignoring image', True);
            except CacheError:
                quietprint('[bobo.image][WARNING]: cache error during download - ignoring image', True);                
            except IOError:
                quietprint('[bobo.image][WARNING]: IO error during download - ignoring image', True);                
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


