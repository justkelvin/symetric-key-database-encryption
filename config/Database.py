#!/usr/bin/env python3

# imports go here
import sys
import mariadb

class Database:
    server_host = ''
    db_name = ''
    db_user = ''
    db_password = ''
    connection = ''

    def __init__(self, server_host, db_user, db_password, db_name) -> None:
        self.server_host = server_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name

    def db_connection(self):
        try:
            mydb = mariadb.connect(
                host=self.server_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )
            cursor = mydb.cursor()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        return mydb, cursor
