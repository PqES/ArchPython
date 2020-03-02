from database import Database
import pymongo

#nome de variavel = sql, query, database
#import mysql, database
#string = "insert into", "select * from", "update from", "delete from"
#dao no Nome Da Classe
#dao no nome do arquivo

class DAOUser:

    def __init__(self):

        self.database = Database()
    
    def create_user(self, user):
        name, description = user.get_name(), user.get_description()

        sql = 'insert into users (name, description) values ("'+name+'", "'+description+'");'

        if (self.database.execute_query(sql)):
            return True
        return False
    
    def get_users(self):

        sql = "select * from users"

        result = self.database.execute_query(sql)

        print(result)

        # if (self.database.execute_query(sql)):
        #     return True
        return result