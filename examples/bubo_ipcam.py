from bubo.camera import Ipcam
from bubo.show import imshow

def main():
    for im in Ipcam('http://www.capecodlivecam.com/image-hyh.jpg'):
        imshow(im, title='ipcam', using='opencv')
  
if __name__ == '__main__':
    main()

  
