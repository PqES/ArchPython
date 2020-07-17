from models.dao.TaskDAO import TaskDAO
from models.domain_objects.TaskModel import TaskModel
from views.TaskView import TaskView
from util.TaskUtil import TaskUtil
from db.database import Database


class TaskController():

    def __init__(self):
        self.user = UserModel()
        self.view = TaskView()
        self.dao = TaskDAO()
    
    def set_user(self, user):
        self.user = user
    
    def show_menu(self, predefined_option=None):
        option_selected = None
        user = self.user

        if predefined_option != None:
            option_selected = predefined_option
        else:
            
            option_selected = self.view.show_menu(user)

        while option_selected != 1 and option_selected != 2 and option_selected != 3 and option_selected != 0:
            self.view.wrong_option()
            option_selected = self.view.display_options()
        
        if option_selected == 1:
            new_task_info = self.view.create_new_task()
            user_id = self.user.id
            description = new_task_info['description']
            due_date = new_task_info['due_date']
            new_task = TaskModel(None ,user_id, description, due_date)
            database = Database().get_database()
            self.db.tasks.insert(new_task)
            self.show_menu()

        elif option_selected == 2:

            all_tasks = self.dao.get_all_user_tasks(user)
            self.view.render_tasks(all_tasks)
            dummy_input = input()
            self.show_menu()
            
        elif option_selected == 3:
            all_tasks = self.dao.get_all_user_tasks(user)
            self.view.render_tasks(all_tasks)
            tasks_dictionary = TaskUtil.get_dictionary_index_objectid()
            choice = self.view.render_choice()

            if choice not in tasks_dictionary.keys():
                self.view.invalid_choice()
                self.show_menu(3)
            
            else :
                self.dao.mark_task_as_completed(tasks_dictionary[choice])
                self.show_menu()
        
        elif option_selected == 0:
            return
                







        