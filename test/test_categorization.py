from bubo.library.categorization.dummy import Dummy
from bubo.task import categorization
from viset.dataset import Viset

if __name__ == '__main__':
    db = Viset('caltech101.h5', strategy='kfold', kfold=2)
    result = categorization(db, algorithm=Dummy)
