from controllers.UserController import UserController
from controllers.TaskController import TaskController

class App():

    def __init__(self):
        self.start()

    def start(self):
        self.user_controller = UserController()
        self.user_controller.show_options()
        user = self.user_controller.get_user_logged()

        self.task_controller = TaskController() 

        self.task_controller.set_user(user)
        self.task_controller.show_menu()



app = App()
