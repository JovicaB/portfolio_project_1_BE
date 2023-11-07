import MySQLdb
import os
import psycopg2

from abc import ABC, abstractmethod


class SingletonDatabase(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonDatabase, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseConnection(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

class Database(ABC):
    def __init__(self, connection):
        self.connection = connection

    @abstractmethod
    def read_data(self, table_name):
        pass

    @abstractmethod
    def save_data(self, sql_query, data):
        pass


class MySqlConnection(DatabaseConnection):
    def connect(self):
        connection = MySQLdb.connect(
            host = os.environ.get('MYSQL_DB_HOST'),
            user="admin",
            password = os.environ.get('MYSQL_DB_PASSWORD'),
            database="portfolio",
            port=10093,
            charset='utf8mb4'
        )
        return connection

    def close(self, connection):
        if connection:
            connection.close()


class PostgresqlConnection(DatabaseConnection):
    def connect(self, dbname, user, password, host, port=5432):
        connection = psycopg2.connect(
            host = os.environ.get('POSTGRESS_DB_HOST'),
            user="admin",
            password = os.environ.get('POSTGRESS_DB_PASSWORD'),
            database="posgresql_database",
            port=5432,
            charset='utf8mb4'
        )
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        return connection

    def close(self, connection):
        if connection:
            connection.close()


class DatabaseManager(metaclass=SingletonDatabase):
    def __init__(self, connection_type):
        self.connection = self.create_connection(connection_type)

    def create_connection(self, connection_type):
        if connection_type == 'mysql':
            return MySqlConnection()
        elif connection_type == 'postgresql':
            return PostgresqlConnection()
        else:
            raise ValueError("Unsupported database connection type")

    def read_data(self, table_name):
        connection = self.connection.connect()
        cursor = connection.cursor()
        sql = f"SELECT * FROM {table_name}"
        cursor.execute(sql)
        data = cursor.fetchall()
        connection.close()
        return data

    def save_data(self, sql_query, data):
        try:
            connection = self.connection.connect()
            cursor = connection.cursor()
            cursor.execute(sql_query, data)
            connection.commit()
            connection.close()
        except Exception as e:
            print(f"An error occurred while saving the data to the database: {e}")
            return None

        return None
