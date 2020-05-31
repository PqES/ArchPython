from random import randint

class A:
    def f(self):
        numero_aleatorio  = randint(0, 101)

        x = Foo()
        b = B()

        resultado = b.g(x, b, numero_aleatorio)

        print(resultado)


class B:

    def g(self, x, y, z):
        c = C()
        c.h(x)
        c.h(y)

        if (z % 2 == 0):
            return Bar()
        else: 
            return Qux()

class C:

    def h(self, y):
        d = D()
        d.m(y)

class D:

    def __init__(self):
        pass
    
    def m(self, var):
        pass


class Foo:

    def __init__(self):
        pass


class Bar:

    def __init__(self):
        pass

class Qux: 

    def __init__(self):
        pass


a = A()
a.f()