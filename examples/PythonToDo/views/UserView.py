class UserView(object):

    @staticmethod
    def wrong_option():
        print("---")
        print("Invalid option")
        print("---")
    
    @staticmethod
    def display_options():
        print("---")
        print("Welcome!")

        print("1 - Login")
        print("2 - Create new user")

        return int(input())
        print("---")
    
    @staticmethod
    def user_created():
        print("User created!")

    @staticmethod
    def get_credentials():

        print("Enter your credentials")
        login = input("Login: ")
        password = input("Password: ")

        return {'login' : login, 'password' : password}
    
    @staticmethod
    def create_new_user():
        name = input("name: ")
        login = input("Login: ")
        password = input("Passoword: ")
        return {'name' : name, 'login' : login, 'password' : password}
    
    @staticmethod
    def user_not_found():
        print("This user does not exist")
    
    @staticmethod
    def user_exists():
        print("User already exists")
    
    @staticmethod
    def render_all_users(users):
        for user in users:
            print(user)
            print("***")


