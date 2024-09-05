import mysql.connector
from mysql.connector import Error

class DatabaseConnector:
    def __init__(self):
        self.connection = None

    def connect(self, host, user, password, database):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            return True
        except Error as e:
            print(f"Error: {e}")
            return False

    def get_tables(self):
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            cursor.execute("SHOW TABLES")
            return cursor.fetchall()

    def get_columns(self, table_name):
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            return cursor.fetchall()

    def get_rows(self, table_name):
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            return cursor.fetchall()


    def disconnect(self):
        if self.connection.is_connected():
            self.connection.close()
