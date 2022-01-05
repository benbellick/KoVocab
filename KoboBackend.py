import sqlite3
import re
from datetime import datetime
from shutil import copyfile
from functools import reduce

class KoboBackend:
    """ This is a simple class to extract vocab word information from a Kobo eReader into
        a standard python dictionary
    """
    def __init__(self, dbPath, create_back_up = True):
        self.dbPath = dbPath
        self.con = sqlite3.connect(dbPath)
        if(create_back_up):
            copyfile(dbPath, dbPath + ".bak")

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
    def delete_words(self, words):
        sql_word_list = reduce(lambda lst, new_word: lst + "'" + new_word + "', ", words, "(")[:-2] + ")"
        sqlStatement = "DELETE FROM WordList WHERE text in " + sql_word_list + ";"
        return self.con.execute(sqlStatement)

