# В этом файле вся работа с SQLite

import sqlite3
import logging
from db_structure import QUERY


class Database:
    def __init__(self, filename):
        self.con = None
        self.cur = None
        self.filename = filename

    def setup(self):
        self.con = sqlite3.connect(self.filename)
        self.cur = self.con.cursor()
        logging.debug('Установлено подключение к SQLite')
        if not self.is_database_ready():
            self.create_structure()

    def is_database_ready(self):
        try:
            self.cur.execute("SELECT id FROM users LIMIT 1")
            return True
        except:
            logging.warning('Пустой файл базы данных. Создание базовой структуры...')
            return False

    def create_structure(self):
        self.cur.executescript(QUERY)
        self.con.commit()