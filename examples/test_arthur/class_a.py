# -*- coding: utf-8 -*-
from class_foo import Foo
from class_b import B

class A:

	def __init__(self):
		print('Sou o construtor da classe A')

	def f(self):
		print('Sou o método f da classe A')
		print('Não tenho parâmetros')
		x = Foo()
		b = B()
		b.g(x, self)

A().f()

