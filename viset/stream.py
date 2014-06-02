import csv
from viset.image import AnnotatedImage    

class Recognition(object):
    """A stream of labeled imagery"""
    _csvfile = None
    
    def __init__(self, csvfile):        
        _csvfile = csvfile
        self.reader = csv.reader(open(_csvfile, 'rb'), delimiter=' ', quotechar='|')

    def __iter__(self):
        return self

    def next(self):
        row = self.reader.next()
        return (AnnotatedImage(row[0]).annotation(category=row[1]), row[1])

    def parse(self, row):
        return AnnotatedImage(row[0]).annotation(category=row[1])

        
    
