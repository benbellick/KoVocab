from KoboBackend import KoboBackend
from WordDefAPI import WordDefAPI 
import nltk
from nltk.corpus import wordnet as wn
from difflib import get_close_matches
from WordData import WordData
from AnkiAPI import AnkiAPI
import sys


def main():
    if len(sys.argv) != 2:
        print("Improper usage: Use python main.py [path_to_db]")
        return
    db_loc = sys.argv[1]
    kobo = KoboBackend(db_loc)
    word_dict_list = kobo.get_all_word_data()
    word_data_list =[WordData(w) for w in word_dict_list]
    get_word_info = lambda word: WordDefAPI.get_word_info(word, [
        word.recovery_lemmatize,
        word.recovery_unpluralize,
        word.recovery_user_guess
    ])
    try:
        word_def_success_list = list(filter(get_word_info, word_data_list))
        AnkiAPI.add_notes(word_def_success_list)
        note_create_success_list = list(filter(lambda word: word.anki_note_add_success, word_def_success_list))
        raw_words_to_remove = [word.raw_word for word in note_create_success_list]
        kobo.delete_words(raw_words_to_remove)
        print("Successfully loaded the following words:")
        print(raw_words_to_remove)

        remaining_words = [word["word"] for word in kobo.get_all_word_data()]
        print("The following words failed for some reason and remain on the Kobo WordList")
        print(remaining_words)
        kobo.close()
    except Exception as e:
        print(e)
        return
    
if __name__=='__main__':
    main()
