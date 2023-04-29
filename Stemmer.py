from urllib.parse import urlparse
from stemming.porter2 import stem
import re


class Stemmer:
    def StemmerInput(self, TextInput):
        InputsStemmed = []
        TextInput = TextInput.strip()   
        words = re.findall(r'\w+', TextInput) 
        StemmedWords = [stem(word) for word in words]  
        TextStemmed = ' '.join(StemmedWords)
        InputsStemmed.append(TextStemmed)
        return InputsStemmed
