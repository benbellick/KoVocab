from datetime import datetime
class WordData:
    def __init__(self, data_dict):
        self.data_dict = data_dict
        init()

    def init(self):
        reg = re.compile("[^a-zA-Z]$")
        word = reg.sub('', self.data_dict['word']).lower()
        #We strip last non-alphanumeric char (e.g. ;,') and lowercase
        self.word = self.data_dict['word']

        self.language = self.data_dict['language']
        
        self.author, self.title = _extract_author_book(self.data_dict['location'])
        
        self.date = datetime.strptime(word_data[3], '%Y-%m-%dT%H:%M:%SZ')

    def _extract_author_book(self, location):
        parts = location.split(' - ')
        if len(parts) != 2:
            raise Exception("WordExtractor: Author and Title could not be split into 2 by -")
        author = parts[0].split('/')[-1]
        title = parts[1].split('.')[0]
        return author, title
