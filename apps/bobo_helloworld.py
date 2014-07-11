from random import random
from pyspark import SparkContext, SparkConf

def sample(p):
    x, y = random(), random()
    return 1 if x*x + y*y < 1 else 0

if 'sc' not in locals():
    spark_conf = SparkConf()
    spark_conf.set('spark.cores.max','4')
    sc = SparkContext(conf=spark_conf,appName='Bobo HelloWorld!')

NUM_SAMPLES = 1E6
count = sc.parallelize(xrange(0, NUM_SAMPLES)).map(sample).reduce(lambda a, b: a + b)
print "[bobo_helloworld]:  Pi is roughly %f" % (4.0 * count / NUM_SAMPLES)



