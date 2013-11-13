import importlib

BACKEND = importlib.import_module('bubo.gui.using_opencv')

def backend(using='pygame'):
    global BACKEND
    BACKEND = importlib.import_module('bubo.gui.using_%s' % using)
    if using == 'pygame':
        figure()  # need figure before opencv camera otherwise segfault. Why?
    
def using(using_='pygame'):
    backend(using_)

def pause():
    BACKEND.pause()
    
def figure(title=None):
    BACKEND.figure(title)

def close(title=None):
    BACKEND.close(title)

def closeall():
    BACKEND.closeall()
    
#def fullscreen():
#    BACKEND.fullscreen()
    
def imshow(im, handle=None):    
    BACKEND.imshow(im, handle)
    
def rectangle(bbox, color='green', caption=None, filled=False, linewidth=1):
    BACKEND.rectangle(bbox, color, caption, filled, linewidth)

def ellipse(bbox, color='green', caption=None, filled=False, linewidth=1):
    BACKEND.ellipse(bbox, color, caption, filled, linewidth)
    
def circle(center, radius, color='green', caption=None, filled=False, linewidth=1):
    BACKEND.circle(center, radius, color, caption, filled, linewidth)
    
def boundingbox(bbox, caption, color='green'):
    rectangle(bbox, caption=caption, filled=False, linewidth=1, color=color)

def tracks(im, bbox, bboxcolor='green', caption=None, captioncolor='red'):
    BACKEND.tracks(im, bbox, bboxcolor, caption, captioncolor)
    
def frame(fr, im=None, color='green', caption=False):
    BACKEND.frame(fr, im, color, caption)

def scatter(fr, im=None, color='green'):
    BACKEND.scatter(fr, im, color)

def text(ij, caption, color):    
    BACKEND.text(ij, caption, color)

def savefig(handle=None, filename=None):
    return BACKEND.savefig(handle, filename)

def opticalflow(im, flow):
    return BACKEND.opticalflow(im, flow)

def sparseflow(im, flow):
    return BACKEND.sparseflow(im, flow)

def disparity(disp, maxdisparity=None):
    return BACKEND.disparity(disp, maxdisparity)

def impolygon(im, poly, color='green'):
    return BACKEND.impolygon(im, poly, color)
