import pymongo

class Database(): 

    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["PythonTodo"]

    def get_database(self):
        return self.mydb