import bubo.show
from bubo.camera import Webcam

# Application
bubo.show.using('opencv')
for im in Webcam(framerate=True, resize=0.5, grey=False):
    bubo.show.imshow(im, handle='Webcam')
  
