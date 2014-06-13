from pyspark import SparkContext
from bobo.recognition import bagofwords
from bobo.viset import lfw
import bobo.image


# Initialize
sc = SparkContext("local[8]", appName='bagofwords')
imstream = lfw.tinystream()
bagofwords(sc.parallelize(imstream))




