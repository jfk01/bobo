import bubo.show
from bubo.camera import Webcam

def main():
    for im in Webcam(framerate=True):
        bubo.show.imshow(im, title='Webcam', using='opencv')
  
if __name__ == '__main__':
    main()

  
