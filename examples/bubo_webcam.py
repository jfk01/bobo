import bubo.show
from bubo.camera import Webcam

def main():
    for im in Webcam(framerate=True, resize=0.5, grey=False):
        bubo.show.imshow(im, handle='Webcam')
  
if __name__ == '__main__':
    main()

  
