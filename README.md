Overview
--------

The BUBO project is a framework for distributed stream processing of computer vision tasks.

Project: BUBO - Computer Vision Platform  
Author: Jeffrey Byrne <jeff@visym.com>  
URL: https://github.com/visym/bubo/  


Design Goals
------------

* BUBO is optimized for stream processing of images and video 
* BUBO is designed for researchers performing interactive analysis of large vision datasets
* BUBO provides a framework for typical computer vision performance evaluations (classification, detection, flow, tracking...)
* BUBO provides seamless caching and parallelization at the application level
* BUBO uses streaming vision datasets (visets) for data locality
* BUBO is designed for easy deployment of vision tasks on a storm production cluster
* BUBO is open source and written in python and C++, and designed for iPython interactive usage


Related Projects
----------------

storm, ipython, joblib, sklearn, samza, mupd8, ecto, ORK (object recognition kitchen), cloudcv.org, graphlab.org


Glossary
--------

* a "viset" is a streaming vision dataset providing a boundless image+annotation tuple stream
* a "stream algorithm" is a directed acyclic graph defining the stream processing which consumes and transforms streams
* an "analysis" is a sink for a stream algorithm, output for interactive study, query or display 
* In STORM terminology, stream algorithms are "bolt graphs", visets are "spouts", analyses are "bolts"  and a viset + stream algorithm + analysis is a "topology"
* In directed acyclic graph (DAG) terminology, stream algorithms are "subgraphs", viset is "source vertex", analysis is "sink vertex", viset + stream algorithm + analysis are "graphs"
* The American (North and South America) horned owls and the Old World eagle-owls make up the genus Bubo.  Owls are renowned for their excellent vision.

Dependencies
------------
numpy
opencv
matplotlib
viset
sklearn
flickrapi
nltk
pygame



