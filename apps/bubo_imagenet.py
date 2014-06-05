from viset.library import imagenet
from pyspark import SparkContext

if 'sc' not in locals():
    sc = SparkContext("local[8]", appName=imagenet.VISET)

csvfile = imagenet.export()
imstream = imagenet.stream()
sc.textFile(csvfile).foreach(lambda x: imstream[x].load())


# sc.textFile(imagenet.export()).filter(lambda x: imstream[x].iscategory('woolly_bear')).count()
# sc.textFile(‘/Volumes/JEBYRNE/visym/cache/imagenet_fall2011/imagenet_fall2011.csv’).filter(lambda x: ‘motor_scooter’ in imagenet.stream()[x].category).foreach(lambda x: imagenet.stream(outdir=‘/Volumes/JEBYRNE/visym/cache/motor_scooter’)[x].load())
