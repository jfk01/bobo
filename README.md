Project: BUBO - Computer Vision Platform  
Author: Jeffrey Byrne <jeff@visym.com>  
URL: https://github.com/visym/bubo/  

Overview
--------

The BUBO project is a set of matlab and python client tools for distributed stream processing of computer vision tasks.
These tools are designed to interface with a Spark cluster for performance analysis of large datasets.


Design Goals
------------

* BUBO is designed for interactive spark based distributed processing of large computer vision datasets 
* BUBO is designed for researchers performing analysis of large image datasets
* BUBO provides a tools for typical computer vision performance evaluations (object recognition and detection)
* BUBO is designed for easy deployment of vision tasks on a spark production cluster
* BUBO is open source and written in python and C++, and designed for iPython interactive usage


Supported Datasets
-------------------

1. ImageNet-Fall2011  
2. Caltech101  
3. Caltech256  
4. ETHZ shapes
5. ETHZ extended shapes
6. MNIST
7. LabelMe3 
8. Pascal VOC 2012 
9. PubFig
10. Labeled Faces in the Wild (LFW)
11. LFW - Deep Funneled
12. LFW - Funneled

Dependencies
------------
Required: numpy, opencv, matplotlib, sklearn  
Optional: flickrapi, nltk, pygame  




