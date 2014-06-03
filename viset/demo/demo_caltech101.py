from viset.library import caltech101
from viset.image import ImageCategoryStream

def main():
    for imcategory in ImageCategoryStream(caltech101.export()):
        imcategory.show()

if __name__ == '__main__':
    main()

  
