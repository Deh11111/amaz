import sqlite3

class Database:
    def __init__(self,database_file):
        self.connection = sqlite3.connect(database_file,check_same_thread=False)
        self.cursor = self.connection.cursor()

    def add_support(self,name,greetings,time,departament,status,):
        with self.connection:
            result = self.cursor.execute("INSERT INTO `chats`,``(`chat_id`) VALUES(?)",())
            return result

    def get_support_info(self,name,)