import bubo.show
from bubo.camera import Webcam

def main():
    bubo.show.using('pygame'); bubo.show.figure()
    for im in Webcam(framerate=True, resize=0.5, grey=True):
        bubo.show.imshow(im, title='Webcam', using='pygame')
  
if __name__ == '__main__':
    main()

  
