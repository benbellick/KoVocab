from datetime import datetime
import re
import nltk
from nltk.corpus import wordnet as wn
from difflib import get_close_matches

class WordData:
    """
    This is a class to encapsulate all of the information needed about a single word.

    Attributes:
        raw_word (string): The original word as found in the text.
        word (string): The word after some potential processing. This processing reflects efforts to make the word appear in a dictionary.
        language (string): The language of the word
        author (string): The author of the book in which the word was found.
        book (string): The book in which the word as found.
        date (Date): The date the word was saved on the Kobo.
        phonetic (string): Phonetic representation of the word.
        audio_url (string): A URL pointing to a sound file containing the word spoken out loud.
        meanings (dictionary[]): A dictionary containing the meanings, parts of speech, example sentences, etc. of the word.
        origin (string): A string explaining the origin of the word.
        def_api_success (bool): Indicates whether the api querry for the word definition succeeded.
        anki_note_add_success: Indicates if word was correctly added to Anki.
    """
    # Install relevant NLTK data
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')
    try:
        nltk.data.find('corpora/omw-1.4')
    except LookupError:
        nltk.download('omw-1.4')

    def __init__(self, data_dict):
        """
        Constructor for WordData.

        Parameters:
            data_dict (dictioanry): A simple dictionary from which to extract info. This dictionary 
            is of identical form to the one returned by KoboBackend.get_all_word_data()
        """
        self.data_dict = data_dict
        self._init()

    def _init(self):
        reg = re.compile("[^a-zA-Z]$")
        self.raw_word = self.data_dict['word']
        word = reg.sub('', self.data_dict['word']).lower()
        #We strip last non-alphanumeric char (e.g. ;,') and lowercase
        self.word = word
        self.language = self.data_dict['language']
        self._extract_author_book(self.data_dict['location'])
        self.date = datetime.strptime(self.data_dict['date'], '%Y-%m-%dT%H:%M:%SZ')

        #These are loaded in by WordDefAPI
        self.phonetic = ""
        self.audio_url = ""
        self.meanings = ""
        self.origin = ""

        #These are used later after data is loaded in
        self.def_api_success = None
        self.anki_note_add_success = None

    def _extract_author_book(self, location):
        parts = location.split(' - ')
        if len(parts) != 2:
            raise Exception("WordData: Author and Title could not be split into 2 by -")
        self.author = parts[0].split('/')[-1]
        self.book = parts[1].split('.')[0]

    #Inspo: https://stackoverflow.com/a/17279278
    def recovery_lemmatize(self):
        """
        This function alters the word attribute by finding similar, but simpler, words via wordnet. 
        This is so that we may attempt another word definition querry with a form of the word that may be better suited.
        """
        possible = []
        for ss in wn.synsets(self.word):
            for lemma in ss.lemmas():
                for w in lemma.derivationally_related_forms():
                    possible.append(w.name())
                for ps in lemma.pertainyms():
                    possible.append(ps.name())
        matches = get_close_matches(self.word, possible)
        if len(matches) > 0:
            self.word = matches[0]
        return None

    def recovery_unpluralize(self):
        """
        This function alters the word attribute by deleting an 's' from the end if there is one present.
        This is so that we may attempt another word definition querry with a form of the word that may be better suited.
        """
        if self.word[-1] == 's':
            self.word = self.word[:-1]
        else:
            #TODO handle error condition
            return

