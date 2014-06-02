import urllib
import urlparse
import string
import os.path
from os import path
import code
import inspect
import IPython
import pdb
import datetime
from time import gmtime, strftime, localtime, clock


def timestamp():
    """Return date and time string in form DDMMMYY_HHMMSS"""
    return string.upper(strftime("%d%b%y_%I%M%S%p", localtime()) + '_%d' % int(1000*clock()))

def isurl(path):
    return urlparse.urlparse(path).scheme != ""

def remkdir(path):
    if os.path.isdir(path) is False:
        os.mkdir(path)
    

def tolist(x):
    if type(x) is list:
        return x
    else:
        return [x]

def filepath2url(filepath):
    """Convert a relative path to an absolute path with a file URI scheme without a hostname (assumed localhost)"""
    return 'file://%s' % path.abspath(filepath)


def isimg(path):
    (filename, ext) = os.path.splitext(path)
    if (ext is not None) and (len(ext) > 0) and (ext.lower() in ['.jpg','.jpeg','.png','.tif','.tiff','.pgm','.ppm','.gif',]):
        return True
    else:
        return False

def isfile(path):
    return os.path.isfile(str(path))

def isviset(obj):
    return (str(type(obj)) in ['<class \'viset.types.Image\'>', '<class \'viset.types.Data\'>'])

def isarchive(filename):
    (filebase, ext) = splitextension(filename)
    if (ext is not None) and (len(ext) > 0) and (ext.lower() in ['.egg','.jar','.tar','.tar.bz2','.tar.gz','.tgz','.tz2','.zip']):
        return True
    else:
        return False

    
def isxml(path):
    (filename, ext) = os.path.splitext(path)
    if (ext is not None) and (len(ext) > 0) and (ext.lower() in ['.xml']):
        return True
    else:
        return False

def ishdf5(path):
    # tables.is_hdf5_file(path)
    # tables.is_pytables_file(path)
    (filename, ext) = os.path.splitext(path)
    if (ext is not None) and (len(ext) > 0) and (ext.lower() in ['.h5']):
        return True
    else:
        return False

def quietprint(mystr, is_verbose):
    if is_verbose:
        print mystr


def dict2querystring(d):
    qs_dict = {}
    for (k,v) in d.iteritems():
        if v is not None:
            qs_dict[k] = v
    return urlparse.unquote(urllib.urlencode(qs_dict))


def cacheroot():        
    cacheroot = os.environ.get('VISYM_CACHE')
    if cacheroot is None:
        cacheroot = path.join(os.environ['HOME'],'.visym')
    return cacheroot
        
def incache(path, cache=cacheroot()):
    return os.path.join(cache, path)

def iscached(path, cache=cacheroot()):
    return os.path.isfile(incache(path, cache))

def urlfragment(url):
	p = urlparse.urlsplit(url)
	p = urlparse.parse_qs(p[3])

def join_fragment(url, frag=''):
    if len(frag) > 0:
        url = url + '#' + frag
    return url
    

def keyboard():
    """return interactive prompt with local namespace of calling function"""
    #code.interact(local=inspect.currentframe(1).f_locals)
    #IPython.start_ipython()
    #http://stackoverflow.com/questions/15669186/using-ipython-as-an-effective-debugger
    #pdb.set_trace() 

    # put this into the package __init__
    #from pdb import set_trace as keyboard
	#import __builtin__
	#__builtin__.keyboard = keyboard


def touch(filename, mystr=''):
    f = open(filename, 'w')
    f.write(str(mystr))
    f.close()


def splitextension(filename):
    (head, tail) = path.split(filename)
    try:
        (base, ext) = string.split(tail,'.',1)  # for .tar.gz    
        ext = '.'+ext
    except:
        base = tail
        ext = None
    return (os.path.join(head, base), ext) # for consistency with splitext
