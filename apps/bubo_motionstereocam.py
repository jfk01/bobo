import bubo.show
from bubo.camera import MotionStereo

for (imobs, imref) in MotionStereo(framerate=True, resize=0.5, grey=True):
    bubo.show.imshow(imobs, handle='Webcam (Left)')
    bubo.show.imshow(imref, handle='Webcam (Right)')    
  
