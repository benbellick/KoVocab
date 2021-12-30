from WordExtractor import WordExtractor
from WordDefAPI import WordDefAPI 
import nltk
from nltk.corpus import wordnet as wn
from difflib import get_close_matches
from WordData import WordData

def main():
    db_loc = '../kobo_clone/KoboReader.sqlite'
    we = WordExtractor(db_loc)
    word_dict_list = we.get_all_word_data()
    word_data_list =[WordData(w) for w in word_dict_list]
    for w in word_data_list:
        if (WordDefAPI.get_word_info(w, [
            w.recovery_lemmatize,
            w.recovery_unpluralize
        ]) is None):
            print(w.word)
if __name__=='__main__':
    main()
