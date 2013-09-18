from bubo.camera import Webcam
from bubo.show import imshow

def main():
  for im in Webcam():
    imshow(im)
  
if __name__ == '__main__':
  main()
  
