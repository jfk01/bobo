import importlib

BACKEND = importlib.import_module('bubo.gui.using_pygame')

def backend(using='pygame'):
    global BACKEND
    BACKEND = importlib.import_module('bubo.gui.using_%s' % using)
    if using == 'pygame':
        figure()  # need figure before opencv camera otherwise segfault. Why?
    
def using(using_='pygame'):
    backend(using_)
    
def figure(title=None):
    global BACKEND
    BACKEND.figure(title)

def close():
    BACKEND.close()

#def fullscreen():
#    BACKEND.fullscreen()
    
def imshow(im, title=None, using=None):    
    global BACKEND
    if using is not None:
        backend(using)
    BACKEND.imshow(im, title)
    
def rectangle(bbox, color='green', caption=None, filled=False, linewidth=1):
    BACKEND.rectangle(bbox, color, caption, filled, linewidth)

def ellipse(bbox, color='green', caption=None, filled=False, linewidth=1):
    BACKEND.ellipse(bbox, color, caption, filled, linewidth)
    
def circle(center, radius, color='green', caption=None, filled=False, linewidth=1):
    BACKEND.circle(center, radius, color, caption, filled, linewidth)
    
def boundingbox(bbox, caption, color='green'):
    rectangle(bbox, caption=caption, filled=False, linewidth=1, color=color)
    
def frame(fr, im=None, color='green', caption=False):
    BACKEND.frame(fr, im, color, caption)

def scatter(fr, im=None, color='green'):
    BACKEND.scatter(fr, im, color)
    
