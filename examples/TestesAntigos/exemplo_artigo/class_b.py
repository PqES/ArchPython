from class_c import C
from class_qux import Qux
from class_bar import Bar

class B:

    def g(self, x, y, z):
        c = C()
        c.h(x)
        c.h(y)

        if (z % 2 == 0):
            return Bar()
        else: 
            return Qux()
