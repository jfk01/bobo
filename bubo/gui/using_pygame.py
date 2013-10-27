import pygame
from PIL import Image
import multiprocessing
import sys
import os

# Window state
IMG = None
SCREEN = None
DRAWQUEUE = multiprocessing.Queue()
DRAWPROCESS = None

def imshow(im, title):
    figure()
    DRAWQUEUE.put(('_imshow', (im, title)))

def rectangle(bbox, color='green', caption=None, filled=False, linewidth=1):
    figure()
    DRAWQUEUE.put(('_rectangle', (bbox, color, caption, filled, linewidth)))

def ellipse(bbox, color='green', caption=None, filled=False, linewidth=1):
    figure()
    DRAWQUEUE.put(('_ellipse', (bbox, color, caption, filled, linewidth)))
    
def circle(center, radius, color, caption, filled=False, linewidth=1):
    figure()
    DRAWQUEUE.put(('_circle', (center, radius, color, caption, filled, linewidth)))

    
def figure(title=None):
    global DRAWPROCESS
    if (DRAWPROCESS is None) or (DRAWPROCESS.is_alive() == False):
        DRAWPROCESS = _mainloop(DRAWQUEUE)

def close():
    global DRAWPROCESS
    if DRAWPROCESS is not None:
        pygame.display.quit()         
        DRAWPROCESS.terminate()
        DRAWPROCESS = None

def fullscreen():        
    figure()
    DRAWQUEUE.put(('_fullscreen', None))
    
    
def tracking(instream, framerate=None):
    # Initialize window
    pygame.init()
    (im, anno) = instream(async=True)[0]
    imsize = (im.get().shape[0], im.get().shape[1])
    screen = pygame.display.set_mode(imsize) 
    pygame.display.set_caption('tracking')
    imshown = im.url()
    img = pygame.image.load(im.url()) 

    # Initialize text
    font = pygame.font.SysFont(None, 12)

    # Update display
    for (im, anno) in instream(async=True):
        print anno        
        if anno['imurl'] != imshown:
            screen.blit(img, (0,0))
            if framerate is not None:
                pygame.time.wait(int(1000*(1.0/framerate)))
            pygame.display.flip() # update the display            
            img = pygame.image.load(im.url())             
            imshown = im.url()
        bbox = (anno['bbox_xmin'], anno['bbox_ymin'], anno['bbox_xmax']-anno['bbox_xmin'], anno['bbox_ymax']-anno['bbox_ymin'])
        pygame.draw.rect(img, (255,0,0), bbox, 1)

        text = font.render('%d' % anno['trackid'], 1, (0, 255, 0))
        textrect = text.get_rect()
        textrect.centerx = bbox[0] 
        textrect.centery = bbox[1]
        img.blit(text, textrect)
        
        #bbox(, imshape=(im.shape[0], im.shape[1]), bboxcaption=anno['trackid'])

            
def _imshow(im, title=None):
    global IMG
    global SCREEN

    if (type(im) is str) and os.path.isfile(im):
        imgfile = im
        im = Image.open(imgfile)  # do not load pixel buffer, just get size
        #SCREEN = pygame.display.set_mode(im.size, pygame.RESIZABLE) 
        SCREEN = pygame.display.set_mode(im.size)         
        if title is not None:
            pygame.display.set_caption(title)
        IMG = pygame.image.load(imgfile) 
        SCREEN.blit(IMG, (0,0))
        pygame.display.flip() # update the display                
    else:
        SCREEN = pygame.display.set_mode(im.shape) 
        if title is not None:
            pygame.display.set_caption(title)
        pygame.surfarray.blit_array(SCREEN, im)
        pygame.display.flip() # update the display                
    pygame.event.set_grab(True)
    pygame.event.set_grab(False)    

    
def _circle(pos, radius, color='green', caption=None, filled=False, linewidth=1):    
    global IMG
    global SCREEN
    
    if filled:
        linewidth = 0
    pygame.draw.circle(SCREEN, pygame.Color(color), pos, radius, linewidth)
    if caption is not None:
        font = pygame.font.SysFont(None, 12)
        text = font.render('%s' % caption, 1, (0, 255, 0))
        textrect = text.get_rect()
        textrect.centerx = pos[0] 
        textrect.centery = pos[1]
        SCREEN.blit(text, textrect)        
    pygame.display.flip() # update the display                

    
def _rectangle(bbox, color='green', caption=None, filled=False, linewidth=1):
    global IMG
    global SCREEN
    
    font = pygame.font.SysFont(None, 12)
    if filled:
        linewidth = 0
    pygame.draw.rect(SCREEN, pygame.Color(color), bbox, linewidth)
    #SCREEN.blit(IMG, (0,0))
    text = font.render('%s' % caption, 1, (0, 255, 0))
    textrect = text.get_rect()
    textrect.centerx = bbox[0] 
    textrect.centery = bbox[1]
    #IMG.blit(text, textrect)
    SCREEN.blit(text, textrect)    
    
    pygame.display.flip() # update the display                

def _ellipse(bbox, color='green', caption=None, filled=False, linewidth=1):
    global IMG
    global SCREEN
    
    font = pygame.font.SysFont(None, 12)
    if filled:
        linewidth = 0
    pygame.draw.ellipse(SCREEN, pygame.Color(color), bbox, linewidth)
    #SCREEN.blit(IMG, (0,0))
    text = font.render('%s' % caption, 1, (0, 255, 0))
    textrect = text.get_rect()
    textrect.centerx = bbox[0] 
    textrect.centery = bbox[1]
    #IMG.blit(text, textrect)
    SCREEN.blit(text, textrect)    
    
    pygame.display.flip() # update the display                
    

def _fullscreen():
    pygame.display.toggle_fullscreen()  # doesn't work

    
def _mainloop(drawqueue):
    def _mainloop_(drawqueue):
        import pygame
        pygame.init()
        pygame.display.set_icon(pygame.image.load('/Users/jebyrne/dev/bubo/data/visym_owl.png'))        

        # Initialize display
        global SCREEN
        SCREEN = pygame.display.set_mode((320, 240))         
        pygame.display.set_caption('Figure')
        pygame.display.flip() # update the display                

        # Event loop
        Clock = pygame.time.Clock()
        done = False
        while not done:
            try:
                # GUI events
                Clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True 
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            done = True 

                # Drawing events
                if not drawqueue.empty():
                    (funcname, args) = drawqueue.get()
                    func = globals()[funcname]
                    if args is not None:
                        func(*args)
                    else:
                        func()

            except KeyboardInterrupt:
                done = True
            except:
                raise
            
        sys.stdout.flush()
        pygame.display.quit()

    p = multiprocessing.Process(target=_mainloop_, args=(drawqueue,))
    p.daemon = True
    p.start()        
    return p


