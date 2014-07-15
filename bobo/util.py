import urllib
import urlparse
import string
import os.path
import numpy as np
import cv2
import cv2.cv as cv
import tempfile
import time
from time import gmtime, strftime, localtime
import sys
import csv
import hashlib
import bobo.viset

global BOBO_VERBOSITY
BOBO_VERBOSITY = 1

def tofilename(s):
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    s = string.replace(s, ' ', '_');
    s = string.replace(s, '-', '_');        
    return "".join(x for x in s if x in valid_chars)


def viset(visetname):
    """Dynamically import requested vision dataset module"""
    try:
        obj = __import__("bobo.viset.%s" % visetname, fromlist=["bobo.viset"])
    except ImportError:
        raise ValueError('Undefined viset "%s"' % visetname)
    return obj

def isexe(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)

def setverbosity(v):
    global BOBO_VERBOSITY
    BOBO_VERBOSITY = v  # GLOBAL!
    

def sha1(filename):
    sha1 = hashlib.sha1()
    f = open(filename, 'rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.hexdigest()


def ndmax(A):
    return np.unravel_index(A.argmax(), A.shape)

def ndmin(A):
    return np.unravel_index(A.argmin(), A.shape)

def ishdf5(path):
    # tables.is_hdf5_file(path)
    # tables.is_pytables_file(path)
    (filename, ext) = os.path.splitext(path)
    if (ext is not None) and (len(ext) > 0) and (ext.lower() in ['.h5']):
        return True
    else:
        return False


def uniform_random_in_range(rng=(0,1)):
    return (rng[1] - rng[0]) * np.random.random_sample() + rng[0]


# <MOVED> tO bobo.geometry
def similarity_imtransform(txy=(0,0), r=0, s=1):
    R = np.mat([[np.cos(r), -np.sin(r), 0], [np.sin(r), np.cos(r), 0], [0,0,1]])
    S = np.mat([[s,0,0], [0, s, 0], [0,0,1]])
    T = np.mat([[0,0,txy[0]], [0,0,txy[1]], [0,0,0]])
    return S*R + T  # composition

def affine_imtransform(txy=(0,0), r=0, sx=1, sy=1, kx=0, ky=0):
    R = np.mat([[np.cos(r), -np.sin(r), 0], [np.sin(r), np.cos(r), 0], [0,0,1]])
    S = np.mat([[sx,0,0], [0, sy, 0], [0,0,1]])
    K = np.mat([[1,ky,0], [kx,1,0], [0,0,1]])
    T = np.mat([[0,0,txy[0]], [0,0,txy[1]], [0,0,0]])
    return K*S*R + T  # composition

def random_affine_imtransform(txy=((0,0),(0,0)), r=(0,0), sx=(1,1), sy=(1,1), kx=(0,0), ky=(0,0)):
    return affine_imtransform(txy=(uniform_random_in_range(txy[0]), uniform_random_in_range(txy[1])),
                              r=uniform_random_in_range(r),
                              sx=uniform_random_in_range(sx),
                              sy=uniform_random_in_range(sy),
                              kx=uniform_random_in_range(kx),
                              ky=uniform_random_in_range(ky))
# </MOVED>

def imtransform(im, A):
    # cv2.warpPerspective(src, M, dsize[, dst[, flags[, borderMode[, borderValue]]]]) -> dst
    return cv2.warpPerspective(im, A, im.shape)
    
def imagesc(im):
    imout = np.copy(im) # unused
    return cv2.normalize(im, imout, 0, 255, cv2.NORM_MINMAX)
    
def filebase(filepath):
    (head, tail) = os.path.split(filepath)    
    (base, ext) = os.path.splitext(tail)
    return base
    
def matread(txtfile):
    """Whitespace separated values defining columns, lines define rows.  Return numpy matrix"""
    with open(txtfile, 'rb') as csvfile:
        M = [np.float32(row.split()) for row in csvfile]
    return np.mat(M)
        
def imlist(imdir):
    return [os.path.abspath(os.path.join(imdir,item)) for item in os.listdir(imdir) if isimg(item)]

def writelist(mylist, outfile):
    with open(outfile, 'w') as f:
        for s in mylist:
            f.write(s + '\n')
    return(outfile)
    

def imsavelist(imdir, outfile):
    filelist = [os.path.join(imdir,item) for item in os.listdir(imdir) if isimg(item)]
    with open(outfile, 'w') as f:
        for s in filelist:
            f.write(s + '\n')
    return(outfile)
    
def csvlist(imdir):
    return [os.path.join(imdir,item) for item in os.listdir(imdir) if iscsv(item)]

def txtlist(imdir):
    return [os.path.join(imdir,item) for item in os.listdir(imdir) if istextfile(item)]


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
  if ext.lower() in ['.jpg','.jpeg','.png','.tif','.tiff','.pgm','.ppm','.gif']:
    return True
  else:
    return False

def iscsv(path):
  (filename, ext) = os.path.splitext(path)
  if ext.lower() in ['.csv','.CSV']:
    return True
  else:
    return False

def isvideo(path):
  (filename, ext) = os.path.splitext(path)
  if ext.lower() in ['.avi','.mp4','.mov','.wmv']:
    return True
  else:
    return False

def isnumpy(obj):
    return ('numpy' in str(type(obj)))
        

def istextfile(path):
  (filename, ext) = os.path.splitext(path)
  if ext.lower() in ['.txt'] and (filename[0] != '.'):
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
  mat = np.asarray(cv.GetMat(im))
  mat = mat.astype(np.uint8)  # force unsigned char for ctypes
  return mat

def opencv2numpy(im):
  return iplimage2numpy(im)

def numpy2iplimage(im):
  return(cv.fromarray(im))

def numpy2opencv(im):
  return numpy2iplimage(im)
  
def bgr2grey(im_bgr):
    imgrey = cv.CreateImage(cv.GetSize(im_bgr), cv.IPL_DEPTH_8U, 1)
    cv.CvtColor(im_bgr, imgrey, cv.CV_BGR2GRAY)
    return imgrey

def bgr2rgb(im_bgr):
    im_rgb = cv.CreateImage(cv.GetSize(im_bgr), cv.IPL_DEPTH_8U, 3)
    cv.CvtColor(im_bgr, im_rgb, cv.CV_BGR2RGB)
    return im_rgb

def isarchive(filename):
    (filebase, ext) = splitextension(filename)
    if (ext is not None) and (len(ext) > 0) and (ext.lower() in ['.egg','.jar','.tar','.tar.bz2','.tar.gz','.tgz','.tz2','.zip','.gz']):
        return True
    else:
        return False


def mkdir(newdir):
    if not os.path.isdir(newdir):
        os.mkdir(newdir)

def tempimage(ext='jpg'):
  return tempfile.mktemp() + '.' + ext

def temppng():
  return tempimage('png')

def tempcsv():
  return tempfile.mktemp() + '.csv'


def imread(imfile):
    return cv2.imread(imfile)

def imresize(im, scale):
    return cv2.resize(im, (0,0), fx=scale, fy=scale, interpolation=cv2.cv.CV_INTER_LINEAR) 

def touch(filename, mystr=''):
    f = open(filename, 'w')
    f.write(str(mystr))
    f.close()

class Stopwatch(object):    
    """Return elapsed processor time in seconds between calls to enter and exit"""
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.elapsed = self.end - self.start
        
def quietprint(mystr, verbosity=1):
    """Unified entry point for logging and console messages"""
    if  (verbosity <= BOBO_VERBOSITY):  # GLOBAL!
        print mystr

def isfile(path):
    return os.path.isfile(str(path))

def isstring(obj):
    return (str(type(obj)) in ['<type \'str\'>', '<type \'unicode\'>'])
        
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

def remkdir(path):
    if os.path.isdir(path) is False:
        os.makedirs(path)
    return path

def splitextension(filename):
    (head, tail) = os.path.split(filename)
    try:
        (base, ext) = string.split(tail,'.',1)  # for .tar.gz    
        ext = '.'+ext
    except:
        base = tail
        ext = None
    return (os.path.join(head, base), ext) # for consistency with splitext
