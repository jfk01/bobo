import pygame

# pygame.display.toggle_fullscreen 
#pygame.display.quit()

def tracking(instream, framerate=None):
    # Initialize window
    pygame.init()
    pygame.font.init()
    (im, anno) = instream(async=True)[0]
    imsize = (im.get().shape[0], im.get().shape[1])
    screen = pygame.display.set_mode(imsize) 
    pygame.display.set_caption('tracking')
    imshown = im.url()
    img = pygame.image.load(im.url()) 

    # Initialize text
    #font = pygame.font.SysFont(None, 12)
    font = pygame.font.Font(None, 12)

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

