from animalDao import DAOanimal

class Modelanimal():

    def __init__(self):
        self.__idx = None
        self.__name = None
        self.__description = None
        self.__marca = None
    
    def set_name(self, name):
        self.__name = name
    
    def set_description(self, description):
        self.__description = description
    
    def set_marca(self, marca):
        self.__marca = marca
    
    def get_marca(self):
        return self.__marca
    
    def get_name(self):
        return self.__name
    
    def get_description(self):
        return self.__description

    def fabricar_animal(self):
        return DAOanimal().create_animal(self)
    
    def get_animals(self):
        return DAOanimal().get_animals()
