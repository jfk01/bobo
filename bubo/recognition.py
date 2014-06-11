import os
from bubo.cache import Cache

def bag_of_words(imtrain, imtest, features, outdir):
    cache = Cache(subdir=outdir)

    # Unique labels
    labels = imtrain.unique()
    
    # Training 
    # generate features by mapping on imtrain
    
    # run kmeans clustering to generate words
    c = spark.mlib.kmeans()
    
    # construct bag of words representation
    #bubo.recognition.
    
    # One vs. rest linear svm
    for lbl in labels:
        c = spark.mlib.svm()    
    
    # Return testing results
    if imtest is not None:
        pass

    # Intermediate results are stored to cache
