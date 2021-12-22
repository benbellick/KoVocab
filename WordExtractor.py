import sqlite3
import re
from datetime import datetime

class WordExtractor:
    """This is a simple class to extract vocab word information from a Kobo eReader"""

    def __init__(self, dbPath):
        self.dbPath = dbPath
        self.con = sqlite3.connect(dbPath)

    def get_all_word_data(self):
        sqlStatement = "SELECT * FROM WordList;"
        return list(map(self._data_zipper, self.con.execute(sqlStatement)))

    def _data_zipper(self, word_data):
        reg = re.compile("[^a-zA-Z]$")
        author, title = self._extract_author_book(word_data[1])
        #We strip last non-alphanumeric char (e.g. ;,') and lowercase
        return {
            "word": reg.sub('', word_data[0]).lower(),
            "title": title,
            "author": author,
            "language": word_data[2],
            "date": datetime.strptime(word_data[3], '%Y-%m-%dT%H:%M:%SZ')
        }

    def _extract_author_book(self, location):
        parts = location.split(' - ')
        if len(parts) != 2:
            raise Exception("WordExtractor: Author and Title could not be split into 2 by -")
        author = parts[0].split('/')[-1]
        title = parts[1].split('.')[0]
        return author, title

