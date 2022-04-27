import nltk
from nltk.tokenize import TweetTokenizer
from nltk import pos_tag
from dictionary import Dictionary
from filter import filter_text as ft


class H2p:
    def __init__(self, dict_path=None):
        self.dict = Dictionary(dict_path)
        self.tokenize = TweetTokenizer().tokenize

    # Method to check if a text line contains a heteronym
    def contains_het(self, text):
        # Filter the text
        text = ft(text)
        # Tokenize
        words = self.tokenize(text)
        # Check match with dictionary
        for word in words:
            if self.dict.contains(word):
                return True
        return False
