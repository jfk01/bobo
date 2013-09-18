Project: BUBO - Computer Vision Platform
Author: Jeffrey Byrne <jeff@visym.com>
URL: https://bitbucket.org/visym/bubo/


Overview
============

The BUBO project is an open source platform for large scale evaluation of computer vision datasets.

BUBO is written in python and provides a standard mechanism for performance evaluation 

BUBO also allows for large scale deployment of image processing tasks (hadoop?)

BUBO provides the same code to run on the desktop as in the cloud

BUBO defines standard computer vision evaluation tasks (classification, detection, detection-polygon)

BUBO takes as inputs a computer vision dataset and an image processing function

BUBO handles caching of intermediate results, exposing functions on the web

BUBO provides standard task APIs to abstract the evaluation process

BUBO is to vision as ROS is to robotics?

BUBO should be used for all image processing on a cluster

BUBO can be used for standard evaluations for CVPR

BUBO is used by visym so we can eat dogfood for our own evaluations

BUBO provides streaming evaluation in hadoop

BUBO provides GUI tools for conflict resolution and correction

BUBO provides tools to download more images from the web via flickr

BUBO provides simple iterators for reading from cameras


Dependencies
============
numpy
opencv
matplotlib
flickrapi
nltk
wxpython
