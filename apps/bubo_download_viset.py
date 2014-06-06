import sys
import argparse

# Command line options
parser = argparse.ArgumentParser(description='Download vision datasets')
parser.add_argument('--viset', type=str, help='Vision Dataset name', default='caltech101')
parser.add_argument('--outdir', type=str, help='Output directory', default=None)
args = parser.parse_args()

# Dynamically Import requested vision dataset module
try:
    viset = __import__("bubo.viset.%s" % args.viset, fromlist=["bubo.viset"])
except ImportError:
    raise

# Download and display
for im in viset.stream(outdir=args.outdir):
    im.show()    
    print '[bubo_download_viset]: category=%s' % im.category

    
