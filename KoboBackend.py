import sqlite3
import re
from datetime import datetime
from shutil import copyfile
from functools import reduce
from os.path import exists

class KoboBackend:
    """ This is a simple class to extract vocab word information from a Kobo eReader into
        a standard python dictionary.

        Attributes:
            db_path (string): The path to the sqlite db file.
            con (Connection): An object representing the sqlite connection to the db pointed to by db_path.
    """
    def __init__(self, db_path, create_back_up = True):
        """
        The constructor for KoboBackend class.

        Parameters:
            db_path (string): The path to the db.
            create_back_up (bool): Optional parameter to create a backup file of the database.
                This is so that any destructive operations are not permanent. Defaults to True.
        """
        self.db_path = db_path
        if not exists(self.db_path) :
            raise ValueError("Provided path to db that does not exist!")
        self.con = sqlite3.connect(db_path)
        if(create_back_up):
            copyfile(db_path, db_path + ".bak")

    def close(self):
        """
        Close the db connection. Must be called before exiting program."
        """
        self.con.close()

    def get_all_word_data(self):
        """
        Retrieve all saved word data from Kobo device.

        The format returned is a list of dictionaries with keys: word, location, language, date."
        """
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
        """
        Delete all saved words from Kobo device which match anything in words.

        Parameters:
            words (string[]): A list of strings to remove.
        """
        #reduce turns ["one", "two"] -> "('one', 'two')" for sql querry
        sql_word_list = reduce(lambda lst, new_word: lst + "'" + new_word + "', ", words, "(")[:-2] + ")"
        sqlStatement = "DELETE FROM WordList WHERE text in " + sql_word_list + ";"
        self.con.execute(sqlStatement)
        self.con.commit()

