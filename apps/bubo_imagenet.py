from viset.library import imagenet
from pyspark import SparkContext

if 'sc' not in locals():
    sc = SparkContext("local[8]", appName=imagenet.VISET)

csvfile = imagenet.export()
imstream = imagenet.stream()
sc.textFile(csvfile).foreach(lambda x: imstream[x].load())


# sc.textFile(imagenet.export()).filter(lambda x: imstream[x].iscategory('woolly_bear')).count()

