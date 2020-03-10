# -*- coding: utf-8 -*-
from class_d import D

class C:

	def __init__(self):
		print('Sou o construtor da classe C')

	def h(self, y):
		print('Sou o método h da classe C')
		print(('Fui chamado com parametro y valendo {} com tipo {}').format(y, type(y)))
		x, m, t, zz = 11, 'bola', D(), None
		y = 'a'
		z = True
		k = None
		w = 1.2
		d = D()
		d.m(y)
