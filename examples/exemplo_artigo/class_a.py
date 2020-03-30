from class_foo import Foo
from class_b import B

class A:

    def __init__(self):
        pass

    def f(self):

        x = Foo()
        b = B()
        b.g(x,self)

if __name__ == "__main__":
    A().f()