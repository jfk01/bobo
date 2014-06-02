from viset.cache import Cache
from viset.show import imshow
from time import sleep
import numpy as np
import numpy.random
from numpy.testing import assert_array_equal

def test_cache():
    c = Cache(verbose=True, refetch=False)

    print '[test_cache]: putting and retrieving an object from cache'        
    obj = np.random.rand(2,2)
    filename = c.put(obj)
    assert_array_equal(obj, c.get(filename))
    assert_array_equal(obj, c[filename]) # keys
    
    
    print '[test_cache]: download an image and retrieve from cache'    
    imshow(c.get('http://upload.wikimedia.org/wikipedia/commons/3/39/Athene_noctua_(cropped).jpg'))
    imshow(c.get('http://upload.wikimedia.org/wikipedia/commons/3/39/Athene_noctua_(cropped).jpg'))

    print '[test_cache]: download archive with item fragment'
    imshow(c.get('http://l2r.cs.uiuc.edu/~cogcomp/Data/Car/CarData.tar.gz#subpath=CarData/TrainImages/pos-1.pgm'))
    imshow(c.get('http://l2r.cs.uiuc.edu/~cogcomp/Data/Car/CarData.tar.gz#subpath=CarData/TrainImages/pos-2.pgm'))
    imshow(c.get('http://l2r.cs.uiuc.edu/~cogcomp/Data/Car/CarData.tar.gz#subpath=CarData/TrainImages/pos-3.pgm'))

    try:
        c.get('http://l2r.cs.uiuc.edu/~cogcomp/Data/Car/CarData.tar.gz#subpath=wrong_path')
    except:
        print 'incorrect URL fragment raises exception correctly'

    print '[test_cache]: size of cache in bytes'
    print c.size()

    #print '[test_cache]: delete cache'
    #c.delete()
    #print c.size()    
  
if __name__ == '__main__':
    print 'nosetest unit testing framework - "sh> nosetests /path/to/file.py -s"'



  
