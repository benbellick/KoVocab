import requests
import json

class WordDefAPI:
    """
    This class is to serve as an interface for the word definition API we are using.
    """
    api_url = 'https://api.dictionaryapi.dev/api/v2/entries/en/' 
        
    @classmethod
    def get_word_info(cls, word, recovery_fns):
    """
    A function to retrieve all word info (definitions, origin, audio, etc.) from the API.

    Parameters:
        word (string): The word to search for
        recovery_fns (func[]): These functions serve as 'backups' in case the querry of the API fails. 
            If it does fail, a function from recovery_fns is called (presumably to alter the word attribute), and 
            the API is tried again. This is repeated until either a querry succeeds, or there are no more recovery_fns, in which case we have failed.
    """
        url = cls.api_url + word.word
        response = requests.get(url)
        status_code = response.status_code
        if(status_code == 200):
            json_response = json.loads(response.text)[0]
            word.phonetic = json_response['phonetic']
            word.audio_url = json_response['phonetics'][0]['audio']
            if 'origin' in json_response:
                word.origin = json_response['origin']
            word.meanings =json_response['meanings']
            word.def_api_success = True
            return True
        if(len(recovery_fns) == 0):
            word.def_api_success = False
            return False
        recovery_fns.pop(0)()
        return cls.get_word_info(word, recovery_fns)
