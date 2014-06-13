import bobo.show
from bobo.camera import Webcam

# Application
bobo.show.using('opencv')
for im in Webcam(framerate=True, resize=0.5, grey=False):
    bobo.show.imshow(im, handle='Webcam')
  
