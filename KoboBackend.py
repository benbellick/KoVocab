import sqlite3
import re
from datetime import datetime

class KoboBackend:
    """ This is a simple class to extract vocab word information from a Kobo eReader into
        a standard python dictionary
    """
    def __init__(self, dbPath):
        self.dbPath = dbPath
        self.con = sqlite3.connect(dbPath)

    def get_all_word_data(self):
        sqlStatement = "SELECT * FROM WordList;"
        return list(map(self._data_zipper, self.con.execute(sqlStatement)))

    def _data_zipper(self, word_data):
        return {
            "word": word_data[0],
            "location": word_data[1],
            "language": word_data[2],
            "date": word_data[3]
        }
