from database import Database
import pymongo

#nome de variavel = sql, query, database
#import mysql, database
#string = "insert into", "select * from", "update from", "delete from"
#dao no Nome Da Classe
#dao no nome do arquivo

class DAOCarro:

    def __init__(self):

        self.database = Database()
    
    def create_carro(self, carro):
        name, description = carro.get_name(), carro.get_description()

        sql = 'insert into carros (name, description) values ("'+name+'", "'+description+'");'

        if (self.database.execute_query(sql)):
            return True
        return False
    
    def get_carros(self):

        sql = "select * from carros"

        result = self.database.execute_query(sql)

        print(result)

        # if (self.database.execute_query(sql)):
        #     return True
        return result