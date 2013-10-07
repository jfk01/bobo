import matplotlib
from matplotlib import pyplot as plt
import numpy as np

matplotlib.rcParams['toolbar']= 'None'
plt.ion()
plt.show()

def imshow(im, title=None):
  plt.clf()
  plt.imshow(im)
  plt.autoscale(tight=True)    
  plt.axis('image')  
  if title is not None:
      plt.title(title)
  plt.draw()

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
