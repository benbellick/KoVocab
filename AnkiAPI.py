import requests
import json
from datetime import datetime

class AnkiAPI:
    """
    This is a class to interact with Anki via the AnkiConnect web server.

    All methods are classmethods, so the class itself need not be instantiated.
    """
    @classmethod
    def add_notes(cls, word_data_lst):
        """
        A function to add notes to the English Vocab deck in Anki.

        Parameters:
            word_data_lst (WordData[]): A list of WordData, as defined in the WordData module.
                It is assumed that the appropriate data has been loaded in already via the definition API.

        Returns:
            void
        """
        notes = list(map(cls._word_data_to_anki, word_data_lst))
        base_req = {
            'action': "addNotes",
            'version': 6,
            'params': {
                "notes":  notes
            }
        }
        response = requests.post('http://localhost:8765', json.dumps(base_req))
        #Look into failures
        for i, resp_code in enumerate(json.loads(response.text)["result"]):
            if resp_code is None:
                base_req = {
                    'action': "addNote",
                    'version': 6,
                    'params': {
                        "note":  notes[i]
                    }
                }
                resp = requests.post('http://localhost:8765', json.dumps(base_req))
                if(cls._is_duplicate(resp)):
                    print("Duplicate word found, treating it as a success")
                    word_data_lst[i].anki_note_add_success = True
                else:
                    print("Error creating card for word " + word_data_lst[i].raw_word + ". Please handle manually. The message is as below")
                    print(json.dumps(resp.text)["error"])
                    word_data_lst[i].anki_note_add_success = False
            else:
                word_data_lst[i].anki_note_add_success = True


    @classmethod
    def _word_data_to_anki(cls, word_data):
        num_of_meanings = len(word_data.meanings)
        if(num_of_meanings > 3):
            print("Warning: " + word_data.word + " has more than 3 meanings. The remainder will be excluded.")
        anki_note_api_form = {
            "deckName": "English Vocab",
            "modelName": "English Book Vocab",
            "fields": {
                "Word": word_data.word,
                "Language": word_data.language,
                "Date": word_data.date.strftime("%m/%d/%Y"),
                "Author": word_data.author,
                "Book": word_data.book,
                "Phonetic": word_data.phonetic,
                "Origin": word_data.origin
            },
            "audio": {
                "url": "http:" + word_data.audio_url,
                "filename": word_data.word + "-pronounce-book.mp3",
                "fields": ["Audio"]
            }
        }
        #word info on anki format is 1-indexed
        #For now, we will only load in the first "definition" returned in meanings from the api
        for i, meaning in enumerate(word_data.meanings):
            if i > num_of_meanings:
                break
            index_str = str(i+1) 
            anki_note_api_form["fields"]["Definition " + index_str] = meaning["definitions"][0]["definition"]
            anki_note_api_form["fields"]["Part of Speech " + index_str] = meaning["partOfSpeech"]
            if "example" in meaning["definitions"][0]:
                anki_note_api_form["fields"]["Example Sentence " + index_str] = meaning["definitions"][0]["example"]
            #TODO: synonyms?
        return anki_note_api_form

    @classmethod
    def _is_duplicate(cls, response):
        common_duplicate_result = {
            "result": None, 
            "error": "cannot create note because it is a duplicate"
        }
        if json.loads(response.text) == common_duplicate_result:
            return True
        return False
