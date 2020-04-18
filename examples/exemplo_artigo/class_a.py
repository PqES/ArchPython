from class_foo import Foo
from class_b import B
from class_d import D
from teste_sub.class_e import E

import os

class A:
    def f(self):
        caminho_atual = os.getcwd()
        x = Foo()
        b = B()
        e = E()
        b.g(x,self)

