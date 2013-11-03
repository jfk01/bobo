import numpy as np
import cv2
import threading, multiprocessing
import sys
from time import sleep
import signal
import matplotlib.cm as cm 
from bubo.util import temppng


WINDOWSTATE = {'focus':None, 'windows':{}}

def _num_windows():
    return len(WINDOWSTATE['windows'])

def _handle(h=None):
    if h is None and WINDOWSTATE['focus'] is not None:
        h = WINDOWSTATE['focus']
    elif h is None: 
        h = 'Figure %d' % int(_num_windows()+1)
    elif type(h) is int:
        h = 'Figure %d' % int(h)
    elif type(h) is not str:
        raise ValueError('window handle must be a string')
    return h

def _eventloop(handle, drawqueue):
    def _sigint_handler(signum, frame):
        cv2.destroyWindow(handle)        
        sys.exit()
    signal.signal(signal.SIGINT, _sigint_handler)
    signal.signal(signal.SIGTERM, _sigint_handler)    
    
    cv2.namedWindow(handle)
    cv2.resizeWindow(handle, 320, 240)
    while cv2.waitKey(10) != 27:  # ESC
        if not drawqueue.empty():
            cv2.imshow(handle, drawqueue.get())
    cv2.destroyWindow(handle)

def _flip(im, handle=None):
    if im.ndim == 2:
        imbgr = cv2.cvtColor(im, cv2.cv.CV_GRAY2BGR)
    else:
        imbgr = im
        
    (x, drawprocess, drawqueue) = WINDOWSTATE['windows'][_handle(handle)]
    while drawqueue.empty() == False:
        sleep(0.01)  
    drawqueue.put(imbgr)
    WINDOWSTATE['windows'][_handle(handle)][0] = imbgr.copy()
    
def figure(handle=None):
    global WINDOWSTATE
    handle = _handle(handle)
    WINDOWSTATE['focus'] = handle
    
    if handle not in WINDOWSTATE['windows'].keys() or WINDOWSTATE['windows'][handle][1].is_alive() == False:
        drawqueue = multiprocessing.Queue()
        drawprocess = multiprocessing.Process(target=_eventloop, args=(handle, drawqueue))
        drawprocess.start()        
        WINDOWSTATE['windows'][handle] = [np.zeros((240,320)), drawprocess, drawqueue] 
    return handle

def close(handle=None):
    global WINDOWSTATE
    handle = _handle(handle)
    if handle in WINDOWSTATE['windows'].keys():
        (im, drawprocess, drawqueue) = WINDOWSTATE['windows'][handle]
        drawprocess.terminate()
        del WINDOWSTATE['windows'][handle]
    
def closeall():
    for h in WINDOWSTATE['windows'].iterkeys():
        (im, drawprocess, drawqueue) = WINDOWSTATE['windows'][h]
        drawprocess.terminate()
    WINDOWSTATE['windows'] = {}

def imshow(im, handle=None):    
    _flip(im, figure(handle))
    
def imbbox(im, xmin, xmax, ymin, ymax, bboxcaption=None):
    pass

def rectangle(bbox, color='green', caption=None, filled=False, linewidth=1):
    global WINDOWSTATE
    im = WINDOWSTATE['windows'][WINDOWSTATE['focus']][0]
    cv2.rectangle(im, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), cv2.cv.Scalar(color[0],color[1],color[2])), 
    WINDOWSTATE['windows'][WINDOWSTATE['focus']][0] = im
    imshow(im)

def ellipse(bbox, color='green', caption=None, filled=False, linewidth=1):
    pass


def circle(center, radius, color, caption, filled=False, linewidth=1):
    global WINDOWSTATE
    im = WINDOWSTATE['windows'][WINDOWSTATE['focus']][0]
    cv2.circle(im, center, radius, cv2.cv.Scalar(color[0],color[1],color[2]))
    WINDOWSTATE['windows'][WINDOWSTATE['focus']][0] = im
    imshow(im)

def _color(c):
    if type(c) is str:
        if c == 'green':
            c = cv2.cv.Scalar(0,255,0)
        elif c == 'red':
            c = cv2.cv.Scalar(0,0,255)            
        elif c == 'blue':
            c = cv2.cv.Scalar(255,0,0)            
        else:
            print 'undefined color %s' % c
            c = cv2.cv.Scalar(0,0,0)            
    else:    
        pass
    return c

def _im2bgr(im):
    if im.ndim == 2:
        im = cv2.cvtColor(im, cv2.cv.CV_GRAY2BGR)
    return im    

def frame(fr, im, color, caption):
    im = _im2bgr(im)
    c = _color(color)
    for xysr in fr.transpose():
        bbox = (xysr[0], xysr[1], 10, 10)
        s = xysr[2]
        th = xysr[3]
        R = np.mat([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        x = np.mat([ [-10, +10, +10, -10], [-10, -10, +10, +10] ])
        y = R*((s/10)*x)
        v = [(int(xysr[0]+y[0,0]),int(xysr[1]+y[1,0])), (int(xysr[0]+y[0,1]),int(xysr[1]+y[1,1])), (int(xysr[0]+y[0,2]),int(xysr[1]+y[1,2])), (int(xysr[0]+y[0,3]),int(xysr[1]+y[1,3]))]
        cv2.line(im, v[0], v[1], color=c, thickness=1, lineType=cv2.CV_AA) 
        cv2.line(im, v[1], v[2], color=c, thickness=1, lineType=cv2.CV_AA) 
        cv2.line(im, v[2], v[3], color=c, thickness=1, lineType=cv2.CV_AA) 
        cv2.line(im, v[3], v[0], color=c, thickness=1, lineType=cv2.CV_AA)                                     
    _flip(im, figure('frame'))

def tracks(im, bbox, bboxcolor, caption, captioncolor):
    #if caption is not None:
    #    cv2.putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]]) 

    pass
    
def scatter(fr, im, color):
    im = _im2bgr(im)
    #c = _color(color)
    n_frame = fr.shape[1]
    cmap = cm.get_cmap('jet', n_frame) 
    rgb = np.uint8(255*cmap(np.arange(n_frame)))
    for (i,xysr) in enumerate(fr.transpose()):
        cv2.circle(im, (int(xysr[0]),int(xysr[1])), radius=1, color=cv2.cv.Scalar(int(rgb[i,0]), int(rgb[i,1]), int(rgb[i,2])))
    _flip(im, figure('scatter')) # update the display                

def text(ij, caption, color):
    global WINDOWSTATE
    im = WINDOWSTATE['windows'][WINDOWSTATE['focus']][0]
    cv2.putText(im, caption, ij, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.25, color=_color(color), thickness=1, lineType=cv2.CV_AA)
    # getTextSize() for computing ij offsets
    WINDOWSTATE['windows'][WINDOWSTATE['focus']][0] = im
    imshow(im)
    
def savefig(handle=None, filename=None):
    handle = _handle(handle)
    if filename is None:
        filename = temppng()
    cv2.imwrite(filename, WINDOWSTATE['windows'][WINDOWSTATE['focus']][0])
    return filename
    
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
