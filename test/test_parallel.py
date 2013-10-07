from bubo.parallel import vectorize
from bubo.algorithm import test_vectorize

if __name__ == '__main__':
    result = vectorize(test_vectorize)(2,4,c=8)
    print result.get()
    print result.display_outputs()

