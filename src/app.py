#!/usr/bin/env python3

# imports go here
import os
import sys
import hashlib
import cryptography
from cryptography.fernet import Fernet
from config import Database as DB
from dotenv import load_dotenv
    
load_dotenv()

# main class
class App:
    database_instance = ''

    def __init__(self) -> None:
        self.database_instance = DB.Database(
            self.env('MYSQL_DB_HOST'),
            self.env('MYSQL_DB_USER'),
            self.env('MYSQL_DB_PASSWORD'),
            self.env('MYSQL_DB_DATABASE')
        )

    def env(self, key):
        """ Get the value of an environment variable """
        return os.getenv(key)

    def get_data(self):
        """ Get data from database """
        self.mydb, self.cursor = self.database_instance.db_connection()
        query =  f"SELECT * FROM `{self.env('USER_TABLE')}`"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def login(self, email, password):
        """ Login to the application """
        self.mydb, self.cursor = self.database_instance.db_connection()
        password = password.encode('utf-8')
        password = hashlib.sha256(password).hexdigest()
        email = email.encode('utf-8')
        email = hashlib.sha256(email).hexdigest()
        query = f"SELECT * FROM usertable WHERE email='{email}' AND password='{password}'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if len(result) > 0:
            print('Login successful')
        else:
            print('Login failed')
            
    def insert_data(self, name, email, password):
        """ Insert data into database and perform hashing using sha256 """
        password = password.encode('utf-8')
        password = hashlib.sha256(password).hexdigest()
        email = email.encode('utf-8')
        email = hashlib.sha256(email).hexdigest()
        self.mydb, self.cursor = self.database_instance.db_connection()
        query = f"INSERT INTO usertable (name, email, password) VALUES ('{name}', '{email}', '{password}')"
        self.cursor.execute(query)
        self.mydb.commit()
        self.mydb.close()
        print('Data inserted successfully')

    def reset_password(self, email, password):
        """ Reset password using email and encrypt using sha256 """
        self.mydb, self.cursor = self.database_instance.db_connection()
        password = password.encode('utf-8')
        password = hashlib.sha256(password).hexdigest()
        email = email.encode('utf-8')
        email = hashlib.sha256(email).hexdigest()
        query = f"UPDATE usertable SET password='{password}' WHERE email='{email}'"
        self.cursor.execute(query)
        self.mydb.commit()
        self.mydb.close()
        print('Password reset successfully')

