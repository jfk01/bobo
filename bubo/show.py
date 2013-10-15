import matplotlib
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
import cv2.cv as cv
from bubo.util import numpy2iplimage

matplotlib.rcParams['toolbar']= 'None'
plt.ion()
plt.show()

def imshow(im, title=None, use='opencv'):    
    if use == 'matplotlib':
        plt.clf()
        plt.imshow(im, animated=True, interpolation='nearest')
        plt.autoscale(tight=True)    
        plt.axis('image')  
        if title is not None:
            plt.title(title)
        plt.draw()
    elif use == 'opencv':
        cv.ShowImage(title, numpy2iplimage(im))        
    else:
        raise IOError

def imbbox(im, xmin, xmax, ymin, ymax, bboxcaption=None):
    plt.clf()
    plt.imshow(im)
    plt.autoscale(tight=True)
    plt.axis('image')
    plt.hold(True)

    # (x,y) bounding box is right and down, swap to right and up for plot
    plt.axvspan(xmin, xmax, ymin=1-np.float32(ymax/im.shape[0]), ymax=1-np.float32(ymin/im.shape[0]), edgecolor='g', facecolor='white', linewidth=3, fill=True, alpha=0.5, label='test')  

    if bboxcaption is not None:
        plt.text(xmin, ymin, bboxcaption, bbox=dict(facecolor='white', edgecolor='g',alpha=1))
    plt.draw()

def precision_recall(y_precision, x_recall, title=None):
    plt.clf()
    plt.plot(x_recall, y_precision, label='Precision-Recall curve')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.0])
    plt.xlim([0.0, 1.0])
    if title is not None:
        plt.title(title)
    plt.legend(loc="lower left")
    plt.draw()

def imframe(im, fr):
    ax = plt.axes([0,0,1,1])
    b = plt.imshow(im, cmap=cm.gray)
    plt.hold(True)
    plt.plot(fr[0,:],fr[1,:],'b.')
    plt.hold(False)
    plt.axis('off');
    plt.draw()
    
