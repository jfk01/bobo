"""Object cache for URLs with garbage collection"""

import os
from os import path
import hashlib
import numpy
import urlparse
from viset.util import isarchive, isurl, isimg, ishdf5, isfile, quietprint, isnumpy, isstring
import viset.download
import pylab
import string
import shutil
import h5py


# a cache takes uri as input and stores the results in a local cache defined by a cache root
# pass around relative paths to cache which can be dynamically redefined by an absolute path
# a get operation can be performed on a uri which caches and returns a cache id
# if a get is performed on a cacheid then this file is returned directly
# an object can be put manually into the cache (if we have a known cacheid)



class Cache():
    _cacheroot = os.environ.get('VISYM_CACHE')
    if _cacheroot is None:
        _cacheroot = path.join(os.environ['HOME'],'.visym','cache')
    if not path.exists(_cacheroot):
        os.makedirs(_cacheroot)
    _maxsize = None
    _verbose = None
    _strategy = None
    _free_maxctr = 100
    _free_ctr = _free_maxctr
    _cachesize = None  # async result
    _prettyhash = True
    
    def __init__(self, cacheroot=_cacheroot, maxsize=10E9, verbose=True, strategy='lru', refetch=False):
        if cacheroot is not None:
            self._cacheroot = cacheroot
        self._maxsize = maxsize
        self._verbose = verbose
        self._strategy = strategy
        self._refetch = refetch
            
    def __len__(self):
        if self._cachesize is not None:
            return self._cachesize.get()
        else:
            return self.size()
        
    def __repr__(self):
        return str('<viset.cache: cachedir=' + str(self._cacheroot) + '\'>')
    
    def __getitem__(self, uri):
        return self.get(uri)
                        
    def _download(self, url, timeout=None, sha1=None):        
        """Download url and store downloaded file in cache root, returning absolute filename"""
        #self._free()  # garbage collection time?        
        filename = self.abspath(self.key(urlparse.urldefrag(url)[0]))
        url_scheme = urlparse.urlparse(url)[0]
        if url_scheme == 'http':
            viset.download.download(url, filename, verbose=self._verbose, timeout=timeout)                       
        elif url_scheme == 'file':
            shutil.copyfile(url, filename)
        elif url_scheme == 'hdfs':
            raise NotImplementedError('FIXME: support for hadoop distributed file system')                
        else:
            raise NotImplementedError('FIXME: support for URL scheme ' + url_scheme)
        if sha1 is not None:
            bubo.download.verify_sha1(filename, sha1)
        return filename        

    def _hash(self, url, prettyhash=_prettyhash):
        """Compute a SHA1 hash of a url to generate a unique cache filename for a given url"""
        p = urlparse.urlsplit(url)
        urlquery = urlparse.urlunsplit([p[0],p[1],p[2],p[3],None])
        urlpath = urlparse.urlunsplit([p[0],p[1],p[2],None,None])        
        (filename, ext) = viset.util.splitextension(urlpath)
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
                    print '[viset.cache][WARNING]: cachesize is larger than maximum.  Clean resources!'
            quietprint('[viset.cache]: spawning cache garbage collection process', self._verbose)
            self._cachesize = Pool(1).apply_async(self.size(), self._cacheroot)
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
            raise CacheError('[viset.cache][Error]: Key collision! Existing object in cache with key "%s"' % key)
            
        # Numpy object - export to file in cache with provided key
        if isnumpy(obj):
            quietprint('[viset.cache][PUT]: Exporting numpy object to cache with key "' + key + '"', self._verbose)                                                                             
            f = h5py.File(self.abspath(key), 'a')
            f[key] = obj
            f.close()

        # URL - download and save to cache with provided key
        elif isurl(obj):
            quietprint('[viset.cache][PUT]: "%s" key "%s"' % (obj, key), self._verbose)                                                                                             
            filename = self._download(obj, timeout=timeout, sha1=sha1)
            shutil.move(filename, self.abspath(key))
            
        # Unsupported type!
        else:
            raise CacheError('[viset.cache][ERROR]: Unsupported object type for PUT')
            
        # Return cache key 
        return key        

        
    def get(self, uri):
        """Get the value associated with a key from the cache and return object""" 
        if self.iscached(uri) and self._iskey(uri):
            # URI is a cache key, return absolute filename in cache 
            quietprint('[viset.cache][HIT]: key "%s" ' % (uri), True)      
            filename = self.abspath(uri)                
        elif self.iscached(uri):
            # Convert URI to cache key, return absolute filename in cache
            quietprint('[viset.cache][HIT]: "%s" key "%s" ' % (uri, self.key(uri)), True)
            filename = self.abspath(self.key(uri))  
        else:
            quietprint('[viset.cache][MISS]: downloading "%s"... ' % (uri), True)  
            self.discard(uri)
            filename = self.abspath(self.put(uri))

        # Return absolute file
        return filename

    def discard(self, uri):
        """Delete single url from cache"""
        if self.iscached(uri):
            quietprint('[viset.cache]: Removing key "%s" ' % (uri), self._verbose)            
            os.remove(self.abspath(uri))
        elif self.iscached(uri):
            quietprint('[viset.cache]: Removing cached URI "%s" key "%s" ' % (uri, self.key(uri)), self._verbose)
            os.remove(self.abspath(self.key(uri)))
        elif os.path.isdir(self.abspath(uri)):
            quietprint('[viset.cache]: Removing cached directory "%s" ' % (uri), self._verbose)
            shutil.rmtree(self.abspath(self.cacheid(url)))
        else:
            #quietprint('[viset.cache][WARNING]: Key not found "%s" ' % (self.key(uri)), self._verbose)            
            pass

    def load(self, uri):
        filename = self.get(uri)
        if isimg(filename):
            obj = pylab.imread(filename)
        elif ishdf5(filename):
            f = h5py.File(filename, 'r')
            obj = f[self.key(filename)].value  # FIXME: lazy evaluation?              
        else:
            raise CacheError('[viset.cache][ERROR]: unsupported object type for loading key "%s" ' % self.key(uri))
        return obj
        
            
    def delete(self):
        """Delete entire cache"""
        quietprint('[viset.cache]: Deleting all cached data in "' + self._cacheroot + '"', self._verbose)
        shutil.rmtree(self._cacheroot)
        os.makedirs(self._cacheroot)        

    def clean(self):
        """Delete entire cache"""
        self.delete()

    def size(self, source=_cacheroot):
        """Recursively compute the size in bytes of a cache directory: http://snipplr.com/view/47686/"""
        total_size = os.path.getsize(source)
        for item in os.listdir(source):
            itempath = os.path.join(source, item)
            if os.path.isfile(itempath):
                total_size += os.path.getsize(itempath)
            elif os.path.isdir(itempath):
                total_size += self.size(itempath)
        return total_size

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
            (filename, ext) = viset.util.splitextension(path.basename(urlpath))
            key = str(urlhash) + str(ext)
        elif os.path.isfile(obj):
            # within cache?
            filebase = obj.split(self._cacheroot,1)
            if len(filebase) == 2:
                # key is subpath within cache
                key = filebase[1][1:]
            else:
                # key is filename with unique appended hash
                (head, tail) = os.path.split(obj)
                (filename, ext) = viset.util.splitextension(tail)                 
                namehash = hashlib.sha1(tail).hexdigest()                 
                key = filename + '_' + str(namehash[0:7]) + ext
        elif (path.isfile(self.abspath(obj)) or path.isdir(self.abspath(obj))):
            key = obj   # Already a cache key
        elif isstring(obj):
            key = obj   # Use arbitrary string if not file or url
        else:
            raise CacheError('[viset.cache][ERROR]: Unsupported object for constructing key')
        return key
        
    def abspath(self, key):
        """The absolute file path for a cache key"""
        return os.path.join(self._cacheroot, key)
        
    def root(self):
        return(self._cacheroot)            

    def ls(self):
        print os.listdir(self._cacheroot)

    def unpack(self, pkgkey, dirkey=None, sha1=None, cleanup=False):
        """Extract archive file to unpackdir directory, delete archive file and return archive directory"""
        if not self.iscached(pkgkey):
            raise CacheError('[viset.cache][ERROR]: Key not found "%s" ' % pkgkey)
        filename = self.abspath(pkgkey)
        if isarchive(filename):
            if dirkey is None:
                # unpack directory is the filename without the .ext 
                (unpackdir, ext) = viset.util.splitextension(filename)
            else:
                # Use the provided directory in the cache
                unpackdir = self.abspath(dirkey)
            if not path.exists(unpackdir):
                os.makedirs(unpackdir)
                viset.download.extract(filename, unpackdir, sha1=sha1, verbose=self._verbose)
            else:
                quietprint('[viset.cache][HIT]: "%s" unpacked to "%s"' % (pkgkey, dirkey), self._verbose)                
            if cleanup:
                quietprint('[viset.cache]: Deleting archive "%s" ' % (pkgkey), self._verbose)                                
                os.remove(filename)
            return unpackdir
        else:
            raise CacheError('[viset.cache][ERROR]: Key not archive "%s" ' % pkgkey)            

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
        return str('<viset.cache: obj=' + str(type(self.obj)) + ', cached=' + str(self._cache.iscached(self.uri)) + ', key=\'' + str(self._cache.key(self.uri)) + '\'>')

    
    
