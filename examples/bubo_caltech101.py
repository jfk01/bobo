from bubo.library.categorization import UniformRandomLabels, FrequencyDistributedLabels
from bubo.app.categorization import report_categorization
from viset.dataset import Viset, CategorizationViset
from bubo.util import datestamp
import bubo.metric
import sys

# Open caltech101 viset
try:
    db = Viset('caltech101.h5')
except:
    db = Viset(Caltech101(verbose=True).export())

# Create input stream with training testing split
(trainstream, teststream) = db.annotation.categorization.split(strategy='train-test', randomize=True, step=1)

# Allocate output streams
dbsink = CategorizationViset('caltech101_' + datestamp() + '.h5', mode='w')

# Define algorithm list 
algorithms = [UniformRandomLabels(parallel=False), FrequencyDistributedLabels(parallel=False)]

# Streaming map for each algorithm
#report = bubo.util.mdlist(len(folds),len(algorithms)) # preallocate
for (i, algo) in enumerate(algorithms):
    #(ap, f1, pr, y, yhat) = report(algo.train_and_test(fold.train, fold.test, outstream.new()), fold.test)
    outstream = algo.train_and_test(trainstream, teststream, dbsink.output.categorization.new())


# Report overall categorization performance
(ap, f1, confusion, pr, labels) =  report_categorization(outstream)
dbsink.close()

print ap

# Interactive analysis of stream results
#bubo.analysis.display_categorization()



