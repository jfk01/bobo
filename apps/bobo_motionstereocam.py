import bobo.show
from bobo.camera import MotionStereo

for (imobs, imref) in MotionStereo(framerate=True, resize=0.5, grey=True):
    bobo.show.imshow(imobs, handle='Webcam (Left)')
    bobo.show.imshow(imref, handle='Webcam (Right)')    
  
