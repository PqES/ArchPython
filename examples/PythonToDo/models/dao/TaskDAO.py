from db.database import Database
from models.domain_objects.TaskModel import TaskModel
from bson.objectid import ObjectId


class TaskDAO:

    def __init__(self):
        self.db = Database().get_database()
    
    def create_new_task(self, task_model):
        if task_model._id == None:
            task_model._id = ObjectId()
        self.db.tasks.insert(vars(task_model))
    
    def get_all_user_tasks(self, user):
        user_id = user.id
        all_tasks = self.db.tasks.find({'$and' : [{"user_id" : user_id}, {"completed" : False}]})
        tasks_model = []
        for task in all_tasks:
            task_model = TaskModel(task['_id'], user_id, task['task_description'], task['due_date'], task['completed'])
            tasks_model.append(task_model)
        return tasks_model
    
    def mark_task_as_completed(self, objectId):
        self.db.tasks.update_one({"_id" : objectId}, {'$set' : {'completed' : True}})

