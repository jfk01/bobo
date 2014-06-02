import os
import csv
import viset.cache 
import numpy as np
import viset.util
from viset.util import isfile, remkdir
import gzip, struct
from array import array
import numpy
import urlparse
import cv2


def labels(gzfile):
    with gzip.open(gzfile, 'rb') as file:
        magic, size = struct.unpack(">II", file.read(8))
        if magic != 2049:
            raise ValueError('Magic number mismatch, expected 2049,'
                            'got %d' % magic)
        labels = array("B", file.read())
    return labels


def imread(gzfile, index):
    """Read MNIST encoded images, adapted from: https://github.com/sorki/python-mnist/blob/master/mnist/loader.py"""

    # Called from viset.cache when reader='mnist'
    with gzip.open(gzfile, 'rb') as file:
        magic, size, rows, cols = struct.unpack(">IIII", file.read(16))
        if magic != 2051:
            raise ValueError('Magic number mismatch, expected 2051, got %d' % magic)
        file.seek(index*rows*cols + 16)
        image = numpy.asarray(array("B", file.read(rows*cols)).tolist())
        return numpy.reshape(image, (rows,cols))
		

def export(outfile=None, outdir=None, do_json=False):
    TRAIN_IMG_URL = 'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz'
    TRAIN_IMG_SHA1 =  '6c95f4b05d2bf285e1bfb0e7960c31bd3b3f8a7d'
    TRAIN_LBL_URL = 'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz'
    TRAIN_LBL_SHA1 = '2a80914081dc54586dbdf242f9805a6b8d2a15fc'
    TEST_IMG_URL = 'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz'
    TEST_IMG_SHA1 = 'c3a25af1f52dad7f726cce8cacb138654b760d48'
    TEST_LBL_URL = 'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz'
    TEST_LBL_SHA1 = '763e7fa3757d93b0cdec073cef058b2004252c17'

    cache = viset.cache.Cache(outdir)
    VISET = 'mnist'
    viset.util.remkdir(cache.abspath(VISET))
    if outfile is None:
        outfile = cache.abspath('mnist.csv')
    
    # Fetch data necessary to initial construction
    train_img_file = cache.get(TRAIN_IMG_URL, sha1=TRAIN_IMG_SHA1)    
    train_lbl_file = cache.get(TRAIN_LBL_URL, sha1=TRAIN_LBL_SHA1)
    test_img_file = cache.get(TEST_IMG_URL, sha1=TEST_IMG_SHA1)    
    test_lbl_file = cache.get(TEST_LBL_URL, sha1=TEST_LBL_SHA1)
    y_train = labels(train_lbl_file).tolist()
    y_test = labels(test_lbl_file).tolist()
    
    # Write dataset 
    with open(outfile, 'wb') as csvfile:            
        f = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)        
        for k in range(60000):
            imfile = os.path.join(cache.abspath(VISET), 'im_%06d.png' % k)
            cv2.imwrite(imfile, imread(train_img_file, k))
            f.writerow([imfile, str(y_train[k]), str(y_train[k])])
            if (k % 100) == 0:
                print '[viset.library.mnist][%d/%d]: exporting to "%s"' % (k, 60000, imfile)
            
        for k in range(10000):
            imfile = os.path.join(cache.abspath(VISET), 'im_%06d.png' % k+60000)
            cv2.imwrite(imfile, imread(test_img_file, k))
            f.writerow([imfile, str(y_test[k]), str(y_test[k])])            
            if (k % 100) == 0:            
                print '[viset.library.mnist][%d/%d]: exporting to "%s"' % (k, 10000, imfile)
      
    # Cleanup
    return outfile
    
