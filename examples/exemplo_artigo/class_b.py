from class_c import C

class B:

    def __init__(self):
        pass
    
    def g(self, x, z):
        c = C()
        c.h(x)
        c.h(z)