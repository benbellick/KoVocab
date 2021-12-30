from datetime import datetime
import re
import nltk
from nltk.corpus import wordnet as wn
from difflib import get_close_matches
class WordData:
    # Install relevant NLTK data
    try:
        nltk.data.find('wordnet')
    except LookupError:
        nltk.download('wordnet')
    try:
        nltk.data.find('omw-1.4')
    except LookupError:
        nltk.download('omw-1.4')

    def __init__(self, data_dict):
        self.data_dict = data_dict
        self.init()

    def init(self):
        reg = re.compile("[^a-zA-Z]$")
        self.raw_word = self.data_dict['word']
        word = reg.sub('', self.data_dict['word']).lower()
        #We strip last non-alphanumeric char (e.g. ;,') and lowercase
        self.word = word

        self.language = self.data_dict['language']
        
        self._extract_author_book(self.data_dict['location'])
        
        self.date = datetime.strptime(self.data_dict['date'], '%Y-%m-%dT%H:%M:%SZ')

        self.definition = None
        self.example = None

    def _extract_author_book(self, location):
        parts = location.split(' - ')
        if len(parts) != 2:
            raise Exception("WordExtractor: Author and Title could not be split into 2 by -")
        self.author = parts[0].split('/')[-1]
        self.title = parts[1].split('.')[0]

    #Inspo: https://stackoverflow.com/a/17279278
    def recovery_lemmatize(self):
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
        if self.word[-1] is 's':
            self.word = self.word[:-1]
        else:
            #TODO handle error condition
            return
