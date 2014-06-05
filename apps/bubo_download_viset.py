import sys

# Command line parameters
visetname = sys.argv[1]
if len(sys.argv) > 2:
    outdir = sys.argv[2]
else:
    outdir = None
    
# Dynamically Import requested vision dataset module
try:
    viset = __import__("bubo.viset.%s" % visetname, fromlist=["bubo.viset"])
except ImportError:
    raise

# Download and display
for im in viset.stream(outdir=outdir):
    im.show()    
    print '[bubo_download_viset]: category=%s' % im.category

    
