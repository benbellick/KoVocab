import WordExtractor
import WordDefAPI
import nltk
from nltk.corpus import wordnet as wn
from difflib import get_close_matches

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
            print(possible_root(w['word']))

#Inspo: https://stackoverflow.com/a/17279278
def possible_root(word):
    possible = []
    for ss in wn.synsets(word):
        for lemma in ss.lemmas():
            for w in lemma.derivationally_related_forms():
                possible.append(w.name())
            for ps in lemma.pertainyms():
                possible.append(ps.name())
    matches = get_close_matches(word, possible)
    if len(matches) > 0:
        return matches[0]
    return None
    

if __name__=='__main__':
    main()
