import importlib

BACKEND = importlib.import_module('bubo.gui.using_pygame')

def backend(using='pygame'):
    global BACKEND
    BACKEND = importlib.import_module('bubo.gui.using_%s' % using)

def figure(title=None):
    BACKEND.figure(title)

def close():
    BACKEND.close()

#def fullscreen():
#    BACKEND.fullscreen()
    
def imshow(im, title=None):    
    BACKEND.imshow(im, title)
    
def rectangle(bbox, color='green', caption=None, filled=False, linewidth=1):
    BACKEND.rectangle(bbox, color, caption, filled, linewidth)

def ellipse(bbox, color='green', caption=None, filled=False, linewidth=1):
    BACKEND.ellipse(bbox, color, caption, filled, linewidth)
    
def circle(center, radius, color='green', caption=None, filled=False, linewidth=1):
    BACKEND.circle(center, radius, color, caption, filled, linewidth)
    
def boundingbox(bbox, caption, color='green'):
    rectangle(bbox, caption=caption, filled=False, linewidth=1, color=color)
    
