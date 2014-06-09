import csv, os
from bubo.cache import CachedObject, Cache, CacheError
from bubo.show import imshow, imbbox
from bubo.util import isnumpy, quietprint, isstring, isvideo
import httplib, urllib2
from bubo.image import ImageCategory

class Video():
    imframe = None
    cache = None
    
    def __init__(self, imframe=None, cache=Cache()):
        self.imframe = imframe
        self.cache = cache
        
    def __repr__(self):
        return str('<bubo.video: uri="%s">' % (self.cache.abspath(self.imframe)))

    
class VideoCategory():
    video = Video()
    category = None
    frame = 1
    
    def __init__(self, imframe=None, category=None, cache=Cache()):
        self.video = Video(imframe, cache)
        self.category = category
        
    def __repr__(self):
        return str('<bubo.video: uri="%s", category="%s">' % (self.video.cache.abspath(self.video.imframe), self.category))

    def parse(self, row):
        """Parse a row from a viset csv textfile into image and category"""
        rowlist = row.encode('utf-8').split()
        self.category = rowlist[1]
        self.video = Video(rowlist[0], cache=self.cache)        
        return self
    
    def iscategory(self, category):
        return (self.category.lower() == category.lower())
                
    def __iter__(self):
        self.frame = 1
        return self

    def __getitem__(self, item):
        return ImageCategory(self.video.cache.abspath(imframe % item), category=self.category)

    def next(self):
        im =  ImageCategory(self.video.cache.abspath(self.video.imframe % self.frame), category=self.category)
        self.frame = self.frame + 1
        return im

    def __len__(self):
        (head, tail) = os.path.split(self.video.imframe)        
        return len([item for item in os.listdir(head) if os.path.isfile(os.path.join(head, item))])

    
class VideoCategoryStream(object):
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
            return VideoCategory(cache=self._cache).parse(item)
        else:
            # Inefficient method for random stream access
            f = open(self._csvfile, 'r')
            for i in range(item):
                line = f.readline()
                if len(line) == 0:
                    raise IndexError('Invalid index "%d"' % item)  # end of file
            f.close()
            row = line.split()
            return (VideoCategory(row[0], category=row[1], cache=self._cache))        

    def next(self):
        row = self.reader.next()
        return (VideoCategory(row[0], category=row[1], cache=self._cache))

