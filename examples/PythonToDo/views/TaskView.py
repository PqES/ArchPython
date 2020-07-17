class TaskView(object):

    @staticmethod
    def wrong_option():
        print("---")
        print("Invalid option")
        print("---")
    
    @staticmethod
    def show_menu(user):
        print("---")
        print(f"Welcome {user.name}!")

        print("1 - Create new task")
        print("2 - Show all incompleted tasks")
        print("3 - Mark task as completed")
        print("\n")
        print("0 - Quit")

        return int(input())


    @staticmethod
    def create_new_task():
        print("---")

        task_description  = input("What's your task? ")
        due_date  = input("What is the expiration date? (DD/MM/YYYY) ")

        return {"description" : task_description, "due_date" : due_date}
    

    @staticmethod
    def render_tasks(tasks):
        print("User tasks: ")
        for index, task  in enumerate(tasks):
            print("*******")
            print(f"Task #{index} -> {task.task_description}")
            print(f"Due date -> {task.due_date}")
            print(f"Completed -> {task.completed}")
            print("*******\n")
    
    @staticmethod
    def render_choice():
        print("Please, inform the index of the task that was completed")
        choice = int(input())
        return choice

    @staticmethod
    def invalid_choice():
        print("Out of bound index, inform another")
