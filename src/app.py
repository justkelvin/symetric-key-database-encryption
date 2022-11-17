#!/usr/bin/env python3

# imports go here
import hashlib
import os
import sys

import cryptography
import typer
from click import confirm, prompt
from config import Database as DB
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()

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
    
    def get_decrypt(self):
        with open('credentials/key.key', 'rb') as file:
            decryption_key = file.read()
            file.close()
            print(decryption_key)
        return decryption_key

    def get_data(self):
        """ Get data from database """
        self.mydb, self.cursor = self.database_instance.db_connection()
        query =  f"SELECT * FROM `{self.env('USER_TABLE')}`"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def login(self, email = None, password = None):
        """ Login to the application """
        self.mydb, self.cursor = self.database_instance.db_connection()

        # prompt for users password and email
        username = prompt('Enter your username: ')
        if email == None:
            email = input('Enter your email: ')
        if password == None:
            input_password = prompt('Enter your password', hide_input = True)
        
        # query = f"SELECT * FROM usertable WHERE email='{email}' AND password='{password}'"
        query = f"SELECT * FROM usertable WHERE name='{username}'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if len(result) > 0:
            email = list(map(lambda item: item[1], result))
            password = list(map(lambda item: item[2], result))
            for i in email:
                email = i
            for i in password:
                saved_password = i
            with open('credentials/key.key', 'rb') as file:
                enc_key = file.read()
                file.close
            fernet = Fernet(enc_key)
            saved_pass = fernet.decrypt(saved_password)
            if input_password == saved_pass.decode():
                print('Login successful')
            else:
                console.print('Wrong password!', style='bold red')
        else:
            console.print('Login failed', style='bold red')
            
    def signup(self, name = None, email = None, password = None):
        """ Insert data into database and perform hashing using sha256 """
        # prompt for details
        if name == None:
            name = prompt('Enter your name: ')
        if email == None:
            email = prompt('Enter your email: ')
        if password == None:
            password = prompt('Enter your password: ', hide_input = True)
            confirm_password = prompt('Confirm your password: ', hide_input = True)
            if password != confirm_password:
                print('Passwords do not match')
                sys.exit()

        # use the key to encrypt user details
        with open('credentials/key.key', 'rb') as file:
            enc_key = file.read()
            file.close

        fernet = Fernet(enc_key)
        password = fernet.encrypt(password.encode())
        email = fernet.encrypt(email.encode())
        self.mydb, self.cursor = self.database_instance.db_connection()
        query = f"INSERT INTO usertable (name, email, password) VALUES (%s, %s, %s)"
        # ('{name}', '{email}', '{password}')"
        print(email)
        self.cursor.execute(query, (name, email, password))
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

