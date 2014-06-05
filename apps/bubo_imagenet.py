import sys
from bubo.image import ImageCategory
from viset.library import imagenet
import bubo.cache
from pyspark import SparkContext

if 'sc' not in locals():
    sc = SparkContext("local[4]", appName=imagenet.VISET)
imcache = imagenet.cache()
#csvfile = imagenet.export(cache=imcache)
csvfile = '/Users/jebyrne/.visym/cache/imagenet_fall2011/imagenet_fall2011.csv'
sc.textFile(csvfile, 4).foreach(lambda x: ImageCategory(cache=imcache).parse(x).load())
    
