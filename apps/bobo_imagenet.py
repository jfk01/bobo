from bobo.viset import imagenet
from pyspark import SparkContext
import argparse

# Command line options
parser = argparse.ArgumentParser(description='Download vision datasets')
parser.add_argument('--category', type=str, help='Image-Net wordnet id for category', default='n01622352')
parser.add_argument('--outdir', type=str, help='Output directory', default=None)
parser.add_argument('--imagenetdir', type=str, help='ImageNet cache directory', default=None)

args = parser.parse_args()

if 'sc' not in locals():
    sc = SparkContext("local[8]", appName=imagenet.VISET)

csvfile = imagenet.export(outdir=args.imagenetdir)
imstream = imagenet.stream(indir=args.imagenetdir, outdir=args.outdir)

rdd = sc.textFile(csvfile).filter(lambda x: args.category in imstream[x].category)
print "[bobo_imagenet]: There are %d images for category (%s=%s)" % (rdd.count(), args.category, imagenet.category(args.category))
#rdd.foreach(lambda x: imstream[x].load())
