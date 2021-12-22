import requests
import json

class WordDefAPI:

    def __init__(self):
       self.api_url = 'https://api.dictionaryapi.dev/api/v2/entries/en/' 
        
    def get_word_info(self, word):
        url = self.api_url + word
        response = requests.get(url)
        json_response = json.loads(response.text)
        return json_response
