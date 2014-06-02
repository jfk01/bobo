from viset.library.imagenet import ImageNetFall2011
from viset.dataset import Viset
from viset.show import imshow

if __name__ == '__main__':
    dbfile = ImageNetFall2011().export(verbose=True)
    db = Viset(dbfile, verbose=True)
    for (im,annotation) in db.annotation.categorization:
        print 'Image=' + str(annotation['idx_image']) + ' Category=' + annotation['category']
        if im is not None:
            imshow(im)
