"""Object cache for URLs with garbage collection"""

import os
from os import path
import hashlib
import numpy
import urlparse
from viset.util import isarchive, isurl, isimg, ishdf5, isfile
import viset.download
import pylab
import string
import shutil
import h5py

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
    
    def __init__(self, cacheroot=_cacheroot, maxsize=10E9, verbose=True, strategy='lru', refetch=True):
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
    
    def __getitem__(self, url):
        return self.get(url)

    def _url_fragment_options(self, url, sha1=None):
        default_opts = {'sha1':sha1, 'subpath':None, 'reader':None, 'idx':None}
        url_scheme = urlparse.urlparse(url)[0]
        url_fragment = urlparse.urlparse(url)[5]   
        opt = default_opts
        fragment = urlparse.parse_qs(url_fragment)
        for key in fragment.keys():
            if type(fragment[key]) is list:
                opt[key] = fragment[key][0]
            else:
                opt[key] = fragment[key]                
        return opt
  
    def _read(self, filename, reader=None, idx=None):
        """Read filename using supplied custom reader and item index and return object"""
        quietprint('[viset.cache][HIT]: Reading "' + reader + '" encoded object with index "' + str(idx) + '" from file "' + filename + '"', self._verbose)
        if reader == 'h5py':
            f = h5py.File(filename,'r')
            obj = f[idx]  # FIXME: this is a link to an hdf5 object and not a numpy object.  Deep copy?
            return obj
        elif reader == 'universal':
            return pylab.imread(filename)
        elif reader == 'mnist':
            return viset.library.mnist.imread(filename, int(idx))
        else:
            self.quietprint('[viset.cache.read][ERROR]: reader type "' + str(reader) + '" unsupported', self._verbose)
            raise NotImplementedError()
        
    def _unpack(self, filename, unpackdir=None, sha1=None):
        """Extract archive to dirname directory, delete archive file and return archive directory"""
        if isarchive(filename):
            if unpackdir is None:
                (unpackdir, ext) = viset.util.splitextension(filename)
            else:
                unpackdir = self.abspath(unpackdir)
            if not path.exists(unpackdir):
                os.makedirs(unpackdir)
            viset.download.extract(filename, unpackdir, sha1=sha1, verbose=self._verbose)            
            os.remove(filename)
            return unpackdir
        return filename
        
    def _load(self, filename, reader=None, idx=None):
        """Load from filename to an object"""
        if isimg(filename):
            # standard image formats
            obj = pylab.imread(filename)
        elif reader is not None:
            # custom reader defined in querystring
            obj = self._read(filename, reader=reader, idx=idx)  
        elif path.isdir(viset.util.splitextension(filename)[0]):
            # archive directory in cache
            obj = viset.util.splitextension(filename)[0] 
        elif isarchive(filename):
            quietprint('[viset.cache][ERROR]: archive file "' + filename + '" not unpacked to "' + (viset.util.splitextension(filename)[0]), self._verbose)
            raise CacheError()
        elif ishdf5(filename):
            obj = filename
        elif isfile(filename):
            obj = filename
        else:
            quietprint('[viset.cache][ERROR]: could not load filename "' + filename + '"', self._verbose)
            raise CacheError()
        return obj
        
    def _download(self, url, timeout=None):        
        """Download url to cached file according to URL scheme and return filename in cache"""
        self._free()  # garbage collection time?        
        filename = self.abspath(self.cacheid(urlparse.urldefrag(url)[0]))
        url_scheme = urlparse.urlparse(url)[0]
        if url_scheme == 'http':
            viset.download.download(url, filename, verbose=self._verbose, timeout=timeout)                       
        elif url_scheme == 'file':
            pass
        elif url_scheme == 'viset':
            raise NotImplementedError('FIXME: support for viset database queries')                            
        elif url_scheme == 'hdfs':
            raise NotImplementedError('FIXME: support for hadoop distributed file system')                
        else:
            raise NotImplementedError('FIXME: support for URL scheme ' + url_scheme)            
        return filename        

    def _fetch(self, url, sha1=None, timeout=None, cacheid=None):
        """Fetch a url and unpack in cache"""
        urlopts = self._url_fragment_options(url, sha1)
        if isurl(url):            
            if cacheid is None:
                cacheid = self.cacheid(url)
            if not self.iscached(cacheid):
                #quietprint('[viset.cache][MISS]: downloading "' + str(url[0:63] + '...') + '"', self._verbose)                                        
                quietprint('[viset.cache][MISS]: downloading "' + str(url) + '"', self._verbose)                                                        
                filename = self._download(url, timeout)
                if isarchive(filename):
                    quietprint('[viset.cache][MISS]: extracting archive \'' + filename + '\'', self._verbose)
                    filename = self._unpack(filename, unpackdir=cacheid, sha1=urlopts['sha1'])
                    if urlopts['subpath'] is not None:
                        filename = os.path.join(filename, urlopts['subpath'])
            else:
                filename = self.abspath(cacheid)
                #quietprint('[viset.cache][HIT]: fetching "' + filename + '"', self._verbose)                                                     
        elif viset.util.isfile(self.abspath(self.cacheid(url))):            
            filename = self.abspath(self.cacheid(url))
            #quietprint('[viset.cache][HIT]: fetching "' + filename + '"', self._verbose)                                                                 
        elif viset.util.isfile(self.abspath(path.basename(url))):
            filename = self.abspath(path.basename(url))
            #quietprint('[viset.cache][HIT]: fetching "' + filename + '"', self._verbose)                                                                             
        elif viset.util.isfile(path.abspath(url)):
            filename = url
            #quietprint('[viset.cache][HIT]: fetching localhost file "%s"' % filename, self._verbose)                                                                                         
        else:
            # nothing in cache or backing store
            quietprint('[viset.cache][MISS]: "' + url + '" not available in cache', self._verbose)                                     
            return None
        
        quietprint('[viset.cache][HIT]: loading "' + filename + '"', self._verbose)                                         
        return self._load(filename, reader=urlopts['reader'], idx=urlopts['idx'])

    def _hash(self, url, prettyhash=_prettyhash):
        """Compute a SHA1 hash of a url to generate a unique cache filename"""
        p = urlparse.urlsplit(url)
        urlquery = urlparse.urlunsplit([p[0],p[1],p[2],p[3],None])
        urlpath = urlparse.urlunsplit([p[0],p[1],p[2],None,None])        
        (filename, ext) = viset.util.splitextension(urlpath)
        urlopt = self._url_fragment_options(url)
        urlhash = hashlib.sha1(urlquery).hexdigest()
        if prettyhash:    
            return path.basename(filename) + '_' + urlhash[0:7]
        else:
            return urlhash 

    def _free(self):
        """Garbage collection"""
        if self._free_ctr == 0:
            if self._cachesize is not None:
                if self._cachesize.get() > self._maxsize:
                    print 'WARNING: cachesize is larger than maximum.  Clean resources!'
            quietprint('[viset.cache.free]: spawning cache garbage collection process', self._verbose)
            self._cachesize = Pool(1).apply_async(self.size(), self._cacheroot)
            self._free_ctr = self._free_maxctr
        self._free_ctr -= 1

        
    def put(self, obj, async=False, key='obj', filename=None):
        """Put a numpy object into cache and return url""" 
        if 'numpy' not in str(type(obj)):
            if type(obj) in [list, tuple]:
                obj = numpy.array(obj)  # type coersion
            else:
                raise ValueError('numpy object required for caching')                    
        if filename is None:
            byteview = obj.view(numpy.uint8)
            filename = hashlib.sha1(byteview).hexdigest() # byte view sha1
        url = 'file://' + self.abspath(filename + '.h5') + '#reader=h5py&idx=' + key
        if self.iscached(url):
            quietprint('[viset.cache.put][HIT]: "' + self.cacheid(url) + '"', self._verbose)                                                     
        else:
            quietprint('[viset.cache.put][MISS]: writing "' + url + '"', self._verbose)                                                                 
            filename = self.abspath(self.cacheid(url))
            f = h5py.File(filename, 'a')
            f[key] = obj
            f.close()
        return CachedObject(url) if async else url
    
    def get(self, url, sha1=None, async=False, timeout=None, cacheid=None):
        """Get a url from cache with refetching on error and return object""" 
        if async:
            return CachedResult(url, sha1=sha1, verbose=self._verbose, cache=self)
        else:
            return self._fetch(url, sha1=sha1, cacheid=cacheid)            

            try:
                return self._fetch(url, sha1=sha1, cacheid=cacheid)
            except KeyboardInterrupt:
                pass
            except CacheError:
                if self._refetch:
                    quietprint('[viset.cache][ERROR]: cache fetch exception - attempting to discard and refetch ... ', True)  
                    self.discard(url)
                    return self._fetch(url, sha1=sha1)
                else:
                    raise
            except:
                raise
            
    def discard(self, url):
        """Delete single url from cache"""
        if path.isfile(self.abspath(self.cacheid(url))):
            quietprint('[viset.cache]: Removing cached file "' + self.cacheid(url) + '"', self._verbose)            
            os.remove(self.abspath(self.cacheid(url)))
        if path.isdir(self.abspath(self.cacheid(url))):
            quietprint('[viset.cache]: Removing cached directory "' + self.cacheid(url) + '"', self._verbose)                        
            shutil.rmtree(self.abspath(self.cacheid(url)))

    def delete(self):
        """Delete entire cache"""
        quietprint('[viset.cache]: Deleting all cached data in "' + self._cacheroot + '"', self._verbose)
        shutil.rmtree(self._cacheroot)
        os.makedirs(self._cacheroot)        

    def clean(self):
        """Delete entire cache"""
        self.delete()

        
    def size(self, source=_cacheroot):
        """Recursively compute the size of a cache directory: http://snipplr.com/view/47686/"""
        total_size = os.path.getsize(source)
        for item in os.listdir(source):
            itempath = os.path.join(source, item)
            if os.path.isfile(itempath):
                total_size += os.path.getsize(itempath)
            elif os.path.isdir(itempath):
                total_size += self.size(itempath)
        return total_size


    def cacheid(self, url):
        """Return a hash derived cache identifier (relative path) from a URL"""
        if viset.util.isurl(url):
            p = urlparse.urlsplit(url)
            urlquery = urlparse.urlunsplit([p[0],p[1],p[2],p[3],None])        
            urlpath = urlparse.urlunsplit([p[0],p[1],p[2],None,None])
            urlopt = self._url_fragment_options(url)
            urlhash = self._hash(url)
            if urlopt['subpath'] is not None:
                return path.join(urlhash, urlopt['subpath'])
            else:
                (filename, ext) = viset.util.splitextension(path.basename(urlpath))
                return str(urlhash) + str(ext)
        else:
            return url

    def abspath(self, cacheid):
        """The absolute file path for a cacheid"""
        return path.join(self._cacheroot, cacheid)
        
    def iscached(self, url):
        """Return true if a url is in the cache"""
        return path.isfile(self.abspath(self.cacheid(url))) or path.isdir(self.abspath(self.cacheid(url))) or path.isfile(self.abspath(url)) or path.isdir(self.abspath(url))
            
            
def quietprint(mystr, is_verbose):
    if is_verbose:
        print mystr
            

class CachedObject(object):
    """Mirrors Python's AsyncResult class"""
    _obj = None    
    _url = None
    _sha1 = None
    _verbose = False
    _cache = None

    def __init__(self, url, sha1=None, verbose=True, cache=None):
        self._verbose = verbose
        if cache is None:
            self._cache = Cache(verbose=self._verbose)
        else:
            self._cache = cache
        self._url = url
        self._sha1 = sha1        
    
    def successful(self):
        return (self._obj is not None)

    def wait(self, timeout_in_seconds):
        if self._obj is None:
            self._obj = self._cache.get(self._url, sha1=self._sha1, async=False, timeout=timeout_in_seconds)
        return self._obj
    
    def ready(self):
        return (self._obj is not None)

    def url(self):
        return self._url
    
    def get(self):
        if self._obj is None:
            self._obj = self._cache.get(self._url, sha1=self._sha1, async=False)
        return self._obj
        
    def __repr__(self):
        return str('<viset.cache: obj=' + str(type(self._obj)) + ', cached=' + str(self._cache.iscached(self._url)) + ', URL=\'' + str(self._url) + '\'>')        
    

class CachedResult(CachedObject):
    pass

class CacheError(Exception):
    pass
