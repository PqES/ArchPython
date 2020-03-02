from userDAO import DAOUser

class ModelUser():

    def __init__(self):
        self.__idx = None
        self.__name = None
        self.__description = None
    
    def set_name(self, name):
        self.__name = name
    
    def set_description(self, description):
        self.__description = description
    
    def get_name(self):
        return self.__name
    
    def get_description(self):
        return self.__description

    def create_user(self):
        return DAOUser().create_user(self)
    
    def get_users(self):
        return DAOUser().get_users()
