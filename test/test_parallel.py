from bubo.parallel import vectorize

def myfunc(x,y):
    from time import sleep
    import os
    sleep(10)
    print 'x=%d, y=%d' % (x,y)
    return os.getpid()


f = vectorize(myfunc, parallel=8)
result = f(range(8), range(8))
print result

