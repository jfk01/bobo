from viset.library import imagenet
from viset.image import ImageCategoryStream

def main():
    imagenet.download(imagenet.export())

if __name__ == '__main__':
    main()

  
