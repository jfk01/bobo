from bubo.library.nearestneighbor import binarylsh, exact
from bubo.app.nearestneighbor import NearestNeighbor
from bubo.stream import RandomLabeledBinaryVector

# Define application
applications = [NearestNeighbor(binarylsh), NearestNeighbor(exact)]
parameters = [{'num_hashtables':4, 'k_hash':4}]*2
instream = RandomLabeledBinaryVector(dimensionality=128, streamlength=4096, numlabels=8)

# Stream!
for (app, opt) in zip(applications, parameters):
    (outstream, model) = app(opt).retrieval(instream)

print outstream
