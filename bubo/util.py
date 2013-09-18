import urllib
import urlparse
import string
import os.path
import numpy
import cv2.cv as cv
import tempfile

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
