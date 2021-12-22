import sqlite3
import re
from datetime import datetime

class WordExtractor:
    """This is a simple class to extract vocab word information from a Kobo eReader"""

    def __init__(self, dbPath):
        self.dbPath = dbPath
        self.con = sqlite3.connect(dbPath)

    def get_word_volume_id_pairs(self):
        sqlStatement = "SELECT Text, VolumeId FROM WordList;"
        return list(self.con.execute(sqlStatement))

    def get_all_word_data(self):
        sqlStatement = "SELECT * FROM WordList;"
        return map(self._data_zipper, self.con.execute(sqlStatement))


    def _data_zipper(self, word_data):
        reg = re.compile("[^a-zA-Z]$")
        #We strip last non-alphanumeric char (e.g. ;,') and lowercase
        return {
            "word": reg.sub('', word_data[0]).lower(),
            "location": word_data[1],
            "language": word_data[2],
            "date": datetime.strptime(word_data[3], '%Y-%m-%dT%H:%M:%SZ')
        }
        

