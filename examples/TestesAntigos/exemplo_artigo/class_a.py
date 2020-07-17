from random import randint
from class_foo import Foo
from class_b import B

class A:
    
    def f(self):
        n  = randint(0, 101)
        a = Foo()
        b = B()
        r = b.g(a, b, n)
