from class_foo import Foo
from class_b import B
from class_d import D
import os

class A:
    def f(self):
        caminho_atual = os.getcwd()
        x = Foo()
        b = B()
        d = D()
        testeinteiro = 2
        b.g(x,self, testeinteiro)

