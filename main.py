import WordExtractor
import WordDefAPI
import nltk
from nltk.corpus import wordnet as wn

def main():
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    print('hello')
    db_loc = '../kobo_clone/KoboReader.sqlite'
    we = WordExtractor.WordExtractor(db_loc)
    wda = WordDefAPI.WordDefAPI()
    word_data = we.get_all_word_data()
    for w in word_data:
        result = wda.get_word_info(w['word'])
        if(len(result) == 3):
            print("word:")
            print(w['word'])
            print("similar words:")
            possible_other(w['word'])

def possible_other(word):
    for ss in wn.synsets(word):
        for lemma in ss.lemmas():
            for word in lemma.derivationally_related_forms():
                print(word.name())
    

if __name__=='__main__':
    main()
