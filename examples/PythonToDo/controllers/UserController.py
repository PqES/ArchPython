from models.dao.UserDAO import UserDAO
from models.domain_objects.UserModel import UserModel
from views.UserView import UserView

class UserController():

    def __init__(self):
        self.view = UserView()
        self.dao = UserDAO()
        self.user_logged = UserModel()
    
    def show_options(self):
        option_selected = self.view.display_options()
        while option_selected != 1 and option_selected != 2:
            self.view.wrong_option()
            option_selected = self.view.display_options()
        user = None
        if option_selected == 1:
            user = self.login()
        else:
            user = self.create_new_user()
        
        if user == None:
            self.show_options()
        else:
            self.user_logged = user
    
    def get_user_logged(self):
        return self.user_logged

    
    def login(self):
        credentials = self.view.get_credentials()
        login = credentials['login']
        password = credentials['password']
        user = self.dao.check_credentials(login, password)
        if user == None:
            self.view.user_not_found()
            return None
        return user
    
    def create_new_user(self):
        new_user_info = self.view.create_new_user()
        new_user = UserModel(new_user_info['name'], new_user_info['login'], new_user_info['password'])
        user_created = self.dao.add_new_user(new_user)
        if user_created != None:
            return user_created
        else:
            self.view.user_exists()
            return None

    
    def get_all_users(self):
        users = self.dao.get_all_users()
        self.view.render_all_users(users)






        