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


def imlist(imdir):
    return [item for item in os.listdir(imdir) if isimg(item)]


def imlistidx(filelist, idx_in_filename):
    """Return index in list of filename containing index number"""
    return [i for (i, item) in enumerate(filelist) if (item.find('%d' % idx_in_filename) > 0)]


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

def bgr2grey(im_bgr):
    imgrey = cv.CreateImage(cv.GetSize(im_bgr), cv.IPL_DEPTH_8U, 1)
    cv.CvtColor(im_bgr, imgrey, cv.CV_BGR2GRAY)
    return imgrey

def bgr2rgb(im_bgr):
    im_rgb = cv.CreateImage(cv.GetSize(im_bgr), cv.IPL_DEPTH_8U, 3)
    cv.CvtColor(im_bgr, im_rgb, cv.CV_BGR2RGB)
    return im_rgb

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
