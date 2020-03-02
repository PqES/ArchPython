import pymysql
from utils import Utils

class Database:
    def __init__(self):
        ut = Utils()
        host = ut.get_hostKey()
        user = "root"
        password = ""
        db = "TaskManager"

        try:
            self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
            self.cur = None
        except pymysql.MySQLError as error:
            print("An error occured in databse creation")
    
    def open_con(self):
        try:
            self.cur = self.con.cursor()
        except pymysql.MySQLError as error:
            print("An error occurred in cursor opening")
    
    def close_con(self):
        try:
            self.con.close() 
        except pymysql.MySQLError as error:
            print("An error occurred in cursor closing")
    
    def execute_query(self, query):
        try:
            self.open_con()
            result = self.cur.execute(query)
            self.con.commit()
            self.close_con()
            print("Query executed with success")
            return self.cur.fetchall()
        except pymysql.MySQLError as error:
            print("An error occurred while executing the query. Error: " +  str(error))
            return False
        return False
