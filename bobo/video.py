import csv, os
from bobo.cache import CachedObject, Cache, CacheError
from bobo.show import imshow, imbbox
from bobo.util import isnumpy, quietprint, isstring, isvideo, tempcsv
import httplib, urllib2
from bobo.image import ImageCategory


def export(objlist, outfile=None):
    """Export a list of bobo.video objects to a CSV file for external consumption"""
    if outfile is None:
        outfile = tempcsv()
    with open(outfile, 'wb') as csvobj:
        f = csv.writer(csvobj, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for vid in objlist:
            f.writerow(vid.export())
    return outfile


class Video():
    uri = None
    imframe = None
    cache = None
    
    def __init__(self, imframe=None, cache=Cache()):
        self.imframe = imframe
        self.uri = imframe        
        self.cache = cache
        
    def __repr__(self):
        return str('<bobo.video: uri="%s">' % (self.cache.abspath(self.imframe)))

    
class VideoCategory():
    uri = None
    category = None
    frame = None
    cache = None
    
    def __init__(self, uri=None, category=None, cache=Cache()):
        self.uri = uri
        self.category = category
        self.cache = cache
        self.frame = 1
        
    def __repr__(self):
        return str('<bobo.video: uri="%s", category="%s">' % (self.cache.abspath(self.uri), self.category))

    def parse(self, row):
        """Parse a row from a viset csv textfile into image and category"""
        rowlist = row.encode('utf-8').split()
        self.category = rowlist[1]
        self.uri = rowlist[0]
        return self
    
    def iscategory(self, category):
        return (self.category.lower() == category.lower())
                
    def __iter__(self):
        self.num_frames = self.__len__()        
        self.frame = 1
        return self

    def __getitem__(self, item):
        return ImageCategory(self.cache.abspath(self.uri % item), category=self.category)

    def next(self):
        if self.frame <= self.num_frames:
            im =  ImageCategory(self.cache.abspath(self.uri % self.frame), category=self.category)
            self.frame = self.frame + 1
            return im            
        else:
            raise StopIteration()

    def __len__(self):
        (head, tail) = os.path.split(self.cache.abspath(self.uri))
        return len([item for item in os.listdir(head) if os.path.isfile(os.path.join(head, item))])

    def export(self):
        """List suitable for export"""
        return [os.path.join(self.cache.root(), self.uri), self.category]

    
class VideoCategoryStream(object):
    """A stream of labeled imagery"""
    csvfile = None
    cache = None
    reader = None
    
    def __init__(self, csvfile, cache=Cache()):        
        self.csvfile = csvfile
        self.cache = cache

    def __iter__(self):
        self.reader = csv.reader(open(self.csvfile, 'rb'), delimiter=' ', quotechar='|')  # reopen
        return self

    def __getitem__(self, item):
        if isstring(item):
            # assume that item is a row from a viset csv file
            return VideoCategory(cache=self.cache).parse(item)
        else:
            # Inefficient method for random stream access
            f = open(self.csvfile, 'r')
            for i in range(item):
                line = f.readline()
                if len(line) == 0:
                    raise IndexError('Invalid index "%d"' % item)  # end of file
            f.close()
            row = line.split()
            return (VideoCategory(row[0], category=row[1], cache=self.cache))        

    def next(self):
        row = self.reader.next()
        return (VideoCategory(row[0], category=row[1], cache=self.cache))

    
    


    
