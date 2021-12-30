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
            json_response = json.loads(response.text)
            return json_response
        if(len(recovery_fns) == 0):
            #TODO: Need to clarify error here somehow
            return None
        recovery_fns.pop(0)()
        return cls.get_word_info(word, recovery_fns)
