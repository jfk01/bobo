from viset.show import imshow
from viset.library import caltech101
from viset.stream import Recognition

def main():
    for (im,annotation) in Recognition(caltech101.export()):
        imshow(im.get(), title=annotation)

if __name__ == '__main__':
    main()

  
