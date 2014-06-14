import sys
import argparse
import bobo.util

# Command line options
parser = argparse.ArgumentParser(description='Download vision datasets')
parser.add_argument('--viset', type=str, help='Vision Dataset name', default='caltech101')
parser.add_argument('--outdir', type=str, help='Output directory', default=None)
args = parser.parse_args()

# Dynamically Import requested vision dataset module
viset = bobo.util.viset(args.viset)

# Download and display
for im in viset.stream(outdir=args.outdir):
    print '[bobo_download_viset]: category=%s' % im.category    
    im.show()    


    
