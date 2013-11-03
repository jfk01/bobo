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
import multiprocessing
import signal 
import sys
from bubo.util import imresize


def _captureloop(imqueue):
    #def _sigint_handler(signum, frame):
    #    sys.exit()
    #signal.signal(signal.SIGINT, _sigint_handler)
    #signal.signal(signal.SIGTERM, _sigint_handler)    
    cam = cv2.VideoCapture(0)
    while True:
        imqueue.put(cam.read())

class Camera(object):
    CAM = None
    FRAMERATE = False
    TIC = 0
    TOC = 0
    RESIZE = None
    GREY = None
    PROCESS = None
    
class Webcam(Camera):
    def __init__(self, framerate=False, resize=1, grey=False):
        self.CAM = multiprocessing.Queue(maxsize=1)
        self.FRAMERATE = framerate
        self.RESIZE = resize
        self.GREY = grey
        if framerate:
            self.TIC = timeit.default_timer()
        self.PROCESS = multiprocessing.Process(target=_captureloop, args=[self.CAM])
        self.PROCESS.start()

    def __del__(self):
        self.PROCESS.terminate()
        
    def __iter__(self):
        return self

    def _read(self):
        im = self.CAM.get()
        return self.CAM.get() # HACK: for slow processing to get most recent image
        
    def next(self):    
        (rval, im) = self._read()
        if self.RESIZE != 1:
            im = imresize(im, self.RESIZE) 
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
            self.IMPREV = self.IMCURRENT.copy()
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
  
