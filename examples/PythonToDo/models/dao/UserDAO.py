from db.database import Database
from models.domain_objects.UserModel import UserModel

class UserDAO:

    def __init__(self):
        self.db = Database().get_database()
    
    def check_credentials(self, login, password):
        user = self.db.users.find_one({"login" : login, "password" : password})
        if user != None:
            user_model = UserModel(user['name'], user['login'], user['password'])
            user_model.id = user['_id']
            return user_model
        return None
    
    def add_new_user(self, user_model):
        user = self.db.users.find_one({"login" : user_model.login})
        if user == None:
            user_object = {"name" : user_model.name, "login" : user_model.login, "password" : user_model.password}
            id_created = self.db.users.insert(user_object)
            user_model.id = id_created
            return user_model
        else:
            return None
