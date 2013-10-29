import glob
import os
import cv2
import cv2.cv as cv
import numpy
import urllib
import timeit
import time
import bubo.util
import tempfile


class Camera(object):
    CAM = None
    FRAMERATE = False
    TIC = 0
    TOC = 0
    RESIZE = None
    GREY = None
    
class Webcam(Camera):
    def __init__(self, framerate=False, resize=1, grey=False):
        self.CAM = cv2.VideoCapture(0)
        self.FRAMERATE = framerate
        self.RESIZE = resize
        self.GREY = grey
        if framerate:
            self.TIC = timeit.default_timer()
        self.next()
            
    def __iter__(self):
        return self

    def next(self):    
        (rval, im) = self.CAM.read()
        if self.RESIZE != 1:
            im = cv2.resize(im, (0,0), fx=self.RESIZE, fy=self.RESIZE) 
        if self.GREY:
            im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        if self.FRAMERATE:
            self.TOC = timeit.default_timer()
            print '[bubo.camera]: frame rate = ' + str(round(1.0/(self.TOC-self.TIC),1)) + ' Hz'
            self.TIC = self.TOC
        return im



class MotionStereo(Webcam):    
    IMCURRENT = None
    IMPREV = None
    
    def next(self):    
        if self.IMPREV is None:
            self.IMPREV = super(MotionStereo, self).next()
        else:
            self.IMPREV = self.IMCURRENT
        self.IMCURRENT = super(MotionStereo, self).next()
        return (self.IMCURRENT, self.IMPREV)
    
class Ipcam(Camera):
    TMPFILE = None
    def __init__(self, url, imfile=bubo.util.tempimage()):
        self.CAM = url
        self.TMPFILE = imfile
    
    def __iter__(self):
        return self

    def next(self):
        urllib.urlretrieve(self.CAM, self.TMPFILE)
        return cv2.imread(self.TMPFILE)  # numpy
  
