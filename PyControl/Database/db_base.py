import abc
import sqlite3


class DBBase(metaclass=abc.ABCMeta):

    def __init__(self, path):
        self.connection = None
        self.db_path = path

    def open(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            cursor = self.connection.cursor()
            return self.connection, cursor
        except sqlite3.Error as e:
            print(e)

    def close(self):
        if self.connection:
            self.connection.close()