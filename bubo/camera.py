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
    
class Webcam(Camera):
    def __init__(self, framerate = False):
        self.CAM = cv.CaptureFromCAM(-1)
        im = cv.QueryFrame(self.CAM)
        im = cv.QueryFrame(self.CAM)
        self.FRAMERATE = framerate
        if framerate:
            self.TIC = timeit.default_timer()
    
    def __iter__(self):
        return self

    def next(self):    
        im = cv.QueryFrame(self.CAM)
        imgrey = cv.CreateImage(cv.GetSize(im), im.depth, 1)
        cv.CvtColor(im,imgrey, cv.CV_BGR2GRAY)
        if self.FRAMERATE:
            self.TOC = timeit.default_timer()
            print '[bubo.camera]: frame rate = ' + str(round(1.0/(self.TOC-self.TIC),1)) + ' Hz'
            self.TIC = self.TOC
        return bubo.util.iplimage2numpy(imgrey)


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
        imgrey = cv2.imread(self.TMPFILE, 0)  # numpy, greyscale
        return imgrey
  
