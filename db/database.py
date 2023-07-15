import sqlite3
import tkinter as tk
import keyboard
import os


class Database:
    SQL_UPDATE_BAD = "UPDATE Bad SET ({}) WHERE ({})"
    SQL_INSERT_BAD = "INSERT INTO Bad ({}) VALUES ({})"
    SQL_SELECT_BAD = "INSERT INTO `chats`({}) VALUES({})"

    def __init__(self,database_file):
        self.connection = sqlite3.connect(database_file,check_same_thread=False)
        self.cursor = self.connection.cursor()

    def add_support(self , **kwargs):
        query = "INSERT INTO `chats`({}) VALUES({})".format(', '.join(kwargs.keys()), ', '.join(['?'] * len(kwargs)))
        values = tuple(kwargs.values())
        with self.connection:
            result = self.cursor.execute(query, values)
            return result
        
   
    # Returns count of support conversation tries
    def add_suport_to_bad(self , name):

        c.execute(self.SQL_SELECT_BAD, (name))
        row = c.fetchone()
        query = ''
        data = [name]

        if row is not None :
             query = self.SQL_UPDATE_BAD.format('count' , 'name')
             data.append((row[0] + 1))
        else:
             query = self.SQL_INSERT_BAD.format('name' , '?')
             data.append(1)

        c.execute(query , data)
        conn.commit()

        return 1 if row is None else (row[0] + 1) 


conn.close()
