from class_foo import Foo
from class_b import B
from class_d import D
from teste_sub.class_e import E
from graphviz import Digraph
from pymongo import MongoClient


import os

class A:
    def f(self):
        caminho_atual = os.getcwd()
        client = MongoClient()
        g = Digraph('G', filename='hello.gv')
        # x = Foo()
        b = B()
        # e = E()
        b.g(g,client)

