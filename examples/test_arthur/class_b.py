# -*- coding: utf-8 -*-
from class_c import C

class B:

	def __init__(self):
		print('Sou o construtor da classe B')

	def g(self, x, z):
		print('Sou o método g da classe B')
		print(('Fui chamado com parametro x valendo {} com tipo {}').format(x, type(x)))
		print(('Fui chamado com parametro z valendo {} com tipo {}').format(z, type(z)))
		c = C()
		c.h(x)
		c.h(z)
