import urllib
import urlparse
import string
import os.path
import numpy
import cv2.cv as cv
import tempfile
import time
from time import gmtime, strftime, localtime
import sys


def mdlist(m,n):
    return [[None]*n for i in range(m)] # preallocate 2D list of size MxN

def isurl(path):
  return urlparse.urlparse(path).scheme != ""

def tolist(x):
  if type(x) is list:
    return x
  else:
    return [x]
    
def isimg(path):
  (filename, ext) = os.path.splitext(path)
  if ext.lower() in ['.jpg','.jpeg','.png','.tif','.tiff','.pgm','.ppm','.gif',]:
    return True
  else:
    return False

def isxml(path):
  (filename, ext) = os.path.splitext(path)
  if ext.lower() in ['.xml']:
    return True
  else:
    return False

def iplimage2numpy(im):
  mat = numpy.asarray(cv.GetMat(im))
  mat = mat.astype(numpy.uint8)  # force unsigned char for ctypes
  return mat

def numpy2iplimage(im):
  return(cv.fromarray(im))
  
def tempimage():
  return tempfile.mktemp()+'.jpg'


class Stopwatch(object):    
    """Return elapsed processor time in seconds between calls to enter and exit"""
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.elapsed = self.end - self.start
        
    
def timestamp():
    """Return date and time string in form DDMMMYY_HHMMSS"""
    return string.upper(strftime("%d%b%y_%I%M%S%p", localtime()))

def datestamp():
    """Return date and time string in form DDMMMYY"""
    return string.upper(strftime("%d%b%y", localtime()))

def print_update(status):
    status = status + chr(8) * (len(status) + 1)
    print status, # space instead of newline
    sys.stdout.flush()    
