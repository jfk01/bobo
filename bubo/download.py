import sys
from viset.image import ImageCategory
from viset.library import imagenet
import viset.cache
from pyspark import SparkContext


def imagenet_fall2011(outdir=None):
    #sc = SparkContext("local", appName=imagenet.VISET)
    imcache = viset.cache.Cache(cacheroot=outdir, subdir=imagenet.VISET)
    #csvfile = imagenet.export(cache=imcache)

    csvfile = '/Volumes/JEBYRNE/visym/cache/imagenet_fall2011/imagenet_fall2011.csv'
    
    lines = sc.textFile(csvfile, 4)
            
    #imagenet.download(csvfile, imcache)

    lines.foreach(lambda x: ImageCategory(cache=imcache).parse(x).load())
    
