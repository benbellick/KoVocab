import WordExtractor
import WordDefAPI

def main():
    print('hello')
    db_loc = '../kobo_clone/KoboReader.sqlite'
    we = WordExtractor.WordExtractor(db_loc)
    wda = WordDefAPI.WordDefAPI()
    word_data = we.get_all_word_data()
    for word in word_data:
        print(word)
        print(wda.get_word_info(word['word']))


if __name__=='__main__':
    main()
