import random
    

def train_test(n, step=1, randomize=False, stratify=False):
    if stratify is True:
        raise NotImplementedError('FIXME: add split stratification to enforce balanced splits')
    k = range(0, n, step)
    if randomize:
        random.shuffle(k)
    k_train = list(k[:len(k)/2])
    k_test = list(k[len(k)/2:])
    split = {'train':k_train, 'test':k_test, 'validate':None}
    return split

def kfold(n, folds, step=1, randomize=False, stratify=False):
    if stratify is True:
        raise NotImplementedError('FIXME: add split stratification to enforce balanced splits')

    k = range(0,n,step)            
    if randomize:
        random.shuffle(k)
    foldsize = len(k)/folds
    split = []
    for f in range(0,folds):
        u = f*foldsize 
        v = u + foldsize    
        k_test = list(k[u:v])
        k_train = list(k)  # copy required
        k_train[u:v] = []
        split.append({'train':k_train, 'test':k_test, 'validate':None})
    return split

def leave_one_out(n, step=1, randomize=False, stratify=False):
    raise NotImplementedError('FIXME: add leave one out split option')


def leave_zero_out(n, step=1, randomize=False, stratify=False):
    if stratify is True:
        raise NotImplementedError('FIXME: add split stratification to enforce balanced splits')   
    k = range(0, n, step)
    if randomize:
        random.shuffle(k)
    return {'train':k, 'test':None, 'validate':None}
