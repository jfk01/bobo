"""Object cache for URLs with garbage collection"""

import os
from os import path
import hashlib
import numpy
import urlparse
from bobo.util import isarchive, isurl, isimg, ishdf5, isfile, quietprint, isnumpy, isstring, remkdir, splitextension
import bobo.viset.download
import pylab
import string
import shutil
import h5py

class Cache():
    _maxsize = None
    _verbose = None
    _strategy = None
    _free_maxctr = 100
    _free_ctr = _free_maxctr
    _cachesize = None  # async result
    _prettyhash = True
    _cacheroot = None
    
    def __init__(self, cacheroot=None, maxsize=10E9, verbose=True, strategy='lru', refetch=False, subdir=None):
        if cacheroot is not None:
            self.setroot(cacheroot)
        elif os.environ.get('BOBO_CACHE') is not None:
            self.setroot(os.environ.get('BOBO_CACHE'))
        else:
            self.setroot(path.join(os.environ['HOME'],'.visym'))
        if subdir is not None:
            self.setroot(os.path.join(self.root(), subdir))
        self._maxsize = maxsize
        self._verbose = verbose
        self._strategy = strategy
        self._refetch = refetch
        #quietprint('[bobo.cache]: initializing cache with root directory "%s"' % self.root(), verbose)
        
    def __len__(self):
        if self._cachesize is not None:
            return self._cachesize.get()
        else:
            return self.size()
        
    def __repr__(self):
        return str('<bobo.cache: cachedir=' + str(self.root()) + '\'>')
    
    def __getitem__(self, uri):
        return self.get(uri)

    def setroot(self, path):
        self._cacheroot = path
        remkdir(self._cacheroot)
            
    def _download(self, url, timeout=None, sha1=None):        
        """Download url and store downloaded file in cache root, returning absolute filename"""
        #self._free()  # garbage collection time?        
        filename = self.abspath(self.key(urlparse.urldefrag(url)[0]))
        url_scheme = urlparse.urlparse(url)[0]
        if url_scheme in ['http', 'https']:
            bobo.viset.download.download(url, filename, verbose=self._verbose, timeout=timeout, sha1=None)                       
        elif url_scheme == 'file':
            shutil.copyfile(url, filename)
        elif url_scheme == 'hdfs':
            raise NotImplementedError('FIXME: support for hadoop distributed file system')                
        else:
            raise NotImplementedError('FIXME: support for URL scheme ' + url_scheme)
        if sha1 is not None:
            bobo.download.verify_sha1(filename, sha1)
        return filename        

    def _hash(self, url, prettyhash=_prettyhash):
        """Compute a SHA1 hash of a url to generate a unique cache filename for a given url"""
        p = urlparse.urlsplit(url)
        urlquery = urlparse.urlunsplit([p[0],p[1],p[2],p[3],None])
        urlpath = urlparse.urlunsplit([p[0],p[1],p[2],None,None])        
        (filename, ext) = splitextension(urlpath)
        #urlopt = self._url_fragment_options(url)
        urlhash = hashlib.sha1(urlquery).hexdigest()
        if prettyhash:    
            return path.basename(filename) + '_' + urlhash[0:7]
        else:
            return urlhash 

    def _free(self):
        """FIXME: Garbage collection"""
        if self._free_ctr == 0:
            if self._cachesize is not None:
                if self._cachesize.get() > self._maxsize:
                    print '[bobo.cache][WARNING]: cachesize is larger than maximum.  Clean resources!'
            quietprint('[bobo.cache]: spawning cache garbage collection process')
            self._cachesize = Pool(1).apply_async(self.size(), self.root())
            self._free_ctr = self._free_maxctr
        self._free_ctr -= 1

    def _iskey(self, key):
        return path.isfile(self.abspath(key)) or path.isdir(self.abspath(key))        

    # ---- PUBLIC FUNCTIONS --------------------------------------------------------    
    def put(self, obj, key=None, timeout=None, sha1=None):
        """Put a URI or numpy object into cache with the provided cache key"""
        if key is None:
            key = self.key(obj)        
        if self.iscached(key):
            raise CacheError('[bobo.cache][Error]: Key collision! Existing object in cache with key "%s"' % key)
            
        # Numpy object - export to file in cache with provided key
        if isnumpy(obj):
            quietprint('[bobo.cache][PUT]: Exporting numpy object to cache with key "' + key + '"')                                                                             
            f = h5py.File(self.abspath(key), 'a')
            f[key] = obj
            f.close()

        # URL - download and save to cache with provided key
        elif isurl(obj):
            quietprint('[bobo.cache][PUT]: "%s" key "%s"' % (obj, key))                                                                                             
            filename = self._download(obj, timeout=timeout)
            shutil.move(filename, self.abspath(key))

            
            
        # Unsupported type!
        else:
            raise CacheError('[bobo.cache][ERROR]: Unsupported object type for PUT')
            
        # Return cache key 
        return key        
        
    def get(self, uri, sha1=None):
        """Get the value associated with a key from the cache and return object""" 
        if self.iscached(uri) and self._iskey(uri):
            # URI is a cache key, return absolute filename in cache 
            quietprint('[bobo.cache][HIT]: key "%s" ' % (uri))      
            filename = self.abspath(uri)                
        elif self.iscached(uri):
            # Convert URI to cache key, return absolute filename in cache
            quietprint('[bobo.cache][HIT]: "%s" key "%s" ' % (uri, self.key(uri)))
            filename = self.abspath(self.key(uri))  
        elif bobo.util.isurl(uri):
            quietprint('[bobo.cache][MISS]: downloading "%s"... ' % (uri))  
            self.discard(uri)
            filename = self.abspath(self.put(uri))
        else:
            raise CacheError('[bobo.cache][ERROR]: invalid uri "%s"' % uri)
        
        # SHA1 check?
        if sha1 is not None:
            quietprint('[bobo.cache]: Verifying SHA1... ')                          
            if not bobo.viset.download.verify_sha1(filename, sha1):
                quietprint('[bobo.cache][ERROR]: invalid SHA1 - discarding and refetching... ')  
                self.discard(uri)            
                self.get(uri, sha1)  # discard and try again
        
        # Return absolute file
        return filename

    def discard(self, uri):
        """Delete single url from cache"""
        if self.iscached(uri):
            quietprint('[bobo.cache]: Removing key "%s" ' % (self.key(uri)))
            if os.path.isfile(self.abspath(self.key(uri))):
                os.remove(self.abspath(self.key(uri)))
        elif os.path.isdir(self.abspath(uri)):
            quietprint('[bobo.cache]: Removing cached directory "%s" ' % (uri))
            shutil.rmtree(self.abspath(self.cacheid(url)))
        else:
            #quietprint('[bobo.cache][WARNING]: Key not found "%s" ' % (self.key(uri)))            
            pass

    def load(self, uri):
        filename = self.get(uri)
        if isimg(filename):
            obj = pylab.imread(filename)
        elif ishdf5(filename):
            f = h5py.File(filename, 'r')
            obj = f[self.key(filename)].value  # FIXME: lazy evaluation?              
        else:
            try:
                obj = pylab.imread(filename)
            except:
                raise CacheError('[bobo.cache][ERROR]: unsupported object type for loading key "%s" ' % self.key(uri))
        return obj
        
            
    def delete(self):
        """Delete entire cache"""
        quietprint('[bobo.cache]: Deleting all cached data in "' + self.root() + '"')
        shutil.rmtree(self.root())
        os.makedirs(self.root())        

    def clean(self):
        """Delete entire cache"""
        self.delete()

    def size(self, key=None):
        """Recursively compute the size in bytes of a cache directory: http://snipplr.com/view/47686/"""
        if key is None:
            total_size = os.path.getsize(self.root())
            for item in os.listdir(self.root()):
                itempath = os.path.join(self.root(), item)
                if os.path.isfile(itempath):
                    total_size += os.path.getsize(itempath)
                elif os.path.isdir(itempath):
                    total_size += self.size(itempath)
            return total_size
        else:
            if os.path.isfile(self.abspath(self.key(key))):            
                return os.path.getsize(self.abspath(self.key(key)))
            else:
                return 0
            

    def iscached(self, uri):
        """Return true if a uri is in the cache"""
        return path.isfile(self.abspath(self.key(uri))) or path.isdir(self.abspath(self.key(uri)))        
    
    def key(self, obj):        
        """Return a cache key (relative path to file in cache) for an object"""
        if isnumpy(obj):
            # Key is byte view sha1 hash with .h5 extension           
            byteview = obj.view(numpy.uint8)
            key = str(hashlib.sha1(byteview).hexdigest()) + '.h5' 
        elif isurl(obj):
            # key is URL filename with an appended hash (for uniqueness)
            p = urlparse.urlsplit(obj)
            urlquery = urlparse.urlunsplit([p[0],p[1],p[2],p[3],None])        
            urlpath = urlparse.urlunsplit([p[0],p[1],p[2],None,None])
            urlhash = self._hash(obj)
            (filename, ext) = splitextension(path.basename(urlpath))
            key = str(urlhash) + str(ext)
        elif os.path.isfile(obj):
            # within cache?
            filebase = obj.split(self.root(),1)
            if len(filebase) == 2:
                # key is subpath within cache
                key = filebase[1][1:]
            else:
                # key is filename with unique appended hash
                (head, tail) = os.path.split(obj)
                (filename, ext) = splitextension(tail)                 
                namehash = hashlib.sha1(tail).hexdigest()                 
                key = filename + '_' + str(namehash[0:7]) + ext
        elif (path.isfile(self.abspath(obj)) or path.isdir(self.abspath(obj))):
            key = obj   # Already a cache key
        elif isstring(obj):
            key = obj   # Use arbitrary string if not file or url
        else:
            raise CacheError('[bobo.cache][ERROR]: Unsupported object for constructing key')
        return key
        
    def abspath(self, key):
        """The absolute file path for a cache key"""
        return os.path.join(self.root(), key)
        
    def root(self):
        return(self._cacheroot) 

    def ls(self):
        print os.listdir(self.root())

    def unpack(self, pkgkey, unpackto=None, sha1=None, cleanup=False):
        """Extract archive file to unpackdir directory, delete archive file and return archive directory"""
        if not self.iscached(pkgkey):
            raise CacheError('[bobo.cache][ERROR]: Key not found "%s" ' % pkgkey)
        filename = self.abspath(pkgkey)
        if isarchive(filename):
            # unpack directory is the same directory as filename
            if unpackto is None:
                unpackdir = self.root()
            else:
                unpackdir = self.abspath(unpackto)
            if not path.exists(unpackdir):
                os.makedirs(unpackdir)
            bobo.viset.download.extract(filename, unpackdir, sha1=sha1, verbose=self._verbose)                
            if cleanup:
                quietprint('[bobo.cache]: Deleting archive "%s" ' % (pkgkey))                                
                os.remove(filename)
            return unpackdir
        else:
            raise CacheError('[bobo.cache][ERROR]: Key not archive "%s" ' % pkgkey)            

class CacheError(Exception):
    pass


class CachedObject(object):
    """Lazy object"""
    obj = None    
    uri = None
    _cache = None

    def __init__(self, uri, cache=None, verbose=True):
        if cache is None:
            self._cache = Cache(verbose=verbose)
        else:
            self._cache = cache
        self.uri = uri
    
    def load(self):
        if self.obj is None:
            self.obj = self._cache.load(self.uri)
        return self.obj
        
    def __repr__(self):
        return str('<bobo.cache: obj=' + str(type(self.obj)) + ', cached=' + str(self._cache.iscached(self.uri)) + ', key=\'' + str(self._cache.key(self.uri)) + '\'>')

    
    def size(self):
        return self._cache.size(self.uri)

    def filename(self):
        return self._cache.abspath(self._cache.key(self.uri))

    def discard(self):
        return self._cache.discard(self.uri)
        
    
