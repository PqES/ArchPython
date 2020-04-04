from class_foo import Foo
from class_b import B

class A:

    def f(self):
        var = 2
        x = Foo(var)
        b = B()
        b.g(x,self)

