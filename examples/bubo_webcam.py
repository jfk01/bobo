from bubo.camera import Webcam
from bubo.show import imshow

def main():
    for im in Webcam(framerate=True):
        imshow(im, title='Webcam', use='opencv')
  
if __name__ == '__main__':
    main()

  
