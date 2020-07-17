class TaskModel:

    def __init__(self, _id, user_id, task_description, due_date, completed=False):
        self._id = _id
        self.user_id = user_id
        self.task_description = task_description
        self.due_date = due_date
        self.completed = completed
