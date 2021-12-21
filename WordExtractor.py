import sqlite3

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
        data_zipper = lambda word_data : {
            "word": word_data[0],
            "location": word_data[1],
            "language": word_data[2],
            "date": word_data[3]
        }
        return map(data_zipper, self.con.execute(sqlStatement))

