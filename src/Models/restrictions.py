class Restrictions:

    def __init__(self, restrictions : dict):
        self.allowed = []
        self.forbidden = []
        self.required = []

        self.get_restrictions(restrictions)
    
    def get_restrictions(self, restrictions):
        pass