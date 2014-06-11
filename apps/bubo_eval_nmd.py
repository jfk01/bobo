import argparse
import bubo.recognition
from bubo.viset import kthactions
from bubo.video import VideoCategoryStream

# Command line options
parser = argparse.ArgumentParser(description='Evaluate nested motion descriptors')
parser.add_argument('--outdir', type=str, help='Output directory', default=None)
args = parser.parse_args()

# Initialize
(trainset, testset) = kthactions.split(kthactions.export(outdir=args.outdir))
bubo.recognition.bag_of_words(trainset, testset, nmd)

for im in kth:
    im.show()
    
# load dataset
# split
# define algorithms

# this should be bubo_eval_recognition where we pass in datasets and split options



