import requests
import json

class WordDefAPI:
    api_url = 'https://api.dictionaryapi.dev/api/v2/entries/en/' 
        
    @classmethod
    def get_word_info(cls, word, recovery_fns):
        url = cls.api_url + word.word
        response = requests.get(url)
        status_code = response.status_code
        if(status_code == 200):
            json_response = json.loads(response.text)[0]
            word.phonetic = json_response['phonetic']
            word.audio_url = json_response['phonetics'][0]['audio']
            if 'origin' in json_response:
                word.origin = json_response['origin']
            #TODO: Perhaps expand out this to not be dict
            word.meanings =json_response['meanings']
            word.def_api_success = True
            return True
        if(len(recovery_fns) == 0):
            #TODO: Need to clarify error here somehow
            word.def_api_success = False
            return False
        recovery_fns.pop(0)()
        return cls.get_word_info(word, recovery_fns)
