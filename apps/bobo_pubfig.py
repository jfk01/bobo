from viset.library import pubfig
from pyspark import SparkContext

if 'sc' not in locals():
    sc = SparkContext("local[8]", appName=pubfig.VISET)

csvfile = pubfig.export()
imstream = pubfig.load()
sc.textFile(csvfile).foreach(lambda x: imstream[x].load())


# [x.show() for x in pubfig.load() if x.iscategory('Steve_Martin')]
# sc.textFile(pubfig.export()).filter(lambda x: pubfig.load()[x].iscategory('Zach_Braff')).count()


    
