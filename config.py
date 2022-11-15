#!/usr/bin/env python3

# imports go here
import sys
import mariadb

class Database:
    server_host = ''
    db_name = ''
    db_user = ''
    db_password = ''
    connections = ''

    def __init__(self, server_host, db_user, db_password, db_name) -> None:
        self.server_host = server_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    def connect(self):
        try:
            connections = mariadb.connect(
                user=self.db_user,
                password=self.db_password,
                host=self.server_host,
                database=self.db_name
            )
            cursor = connections.cursor()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        return connections, cursor

    def close(self):
        self.connections.close()

    def execute(self, query):
        cursor = self.connections.cursor()
        cursor.execute(query)
        return cursor

    def commit(self):
        self.connections.commit()

    def rollback(self):
        self.connections.rollback()

# main function
def main():
    pass

