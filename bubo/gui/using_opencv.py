import numpy as np
import cv2.cv as cv
from bubo.util import numpy2iplimage

def imshow(im, title=None):    
    cv.ShowImage(title, numpy2iplimage(im))        

def imbbox(im, xmin, xmax, ymin, ymax, bboxcaption=None):
    pass


def show_imgdir(imgdir):
  # >>> nsd.show_imgdir("C:\\jebyrne\\penn\\datasets\\altoids")
  print 'Displaying imagery from directory ' + imgdir 
  imglist = glob.glob(os.path.join(imgdir,'*.jpg'))
  for f in imglist:
    img = cv.LoadImage(f)
    thumbnail = cv.CreateMat(img.height / 8, img.width / 8, cv.CV_8UC3)
    cv.Resize(img, thumbnail)
    cv.NamedWindow('display')
    cv.ShowImage('display', thumbnail)
    cv.WaitKey(1)  # 1ms
  
    
