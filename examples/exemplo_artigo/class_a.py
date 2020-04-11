from class_foo import Foo
from class_b import B, OutroTipo
import os

class A:
    def f(self):
        caminho_atual = os.getcwd()
        x = Foo()
        b = B()
        testeinteiro = 2
        b.g(x,self, testeinteiro)

