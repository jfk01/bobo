from bubo.camera import Ipcam
from bubo.show import imshow
import argparse

parser = argparse.ArgumentParser(description='Display imagery from an IP camera')
parser.add_argument('--url', type=str, help='URL for image display from IPCam', default='http://www.capecodlivecam.com/image-hyh.jpg')
args = parser.parse_args()

for im in Ipcam(args.url):
    imshow(im, handle='ipcam')
  
  
