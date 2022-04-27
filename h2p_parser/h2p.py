import nltk
import re
from nltk.tokenize import TweetTokenizer
from nltk import pos_tag
from dictionary import Dictionary
from filter import filter_text as ft


# Method for formatting phonemes
def format_phonemes(phoneme_str):
    # Surround with { }
    phoneme_str = '{' + phoneme_str + '}'
    return phoneme_str


# Method to use Regex to replace the first instance of a word with its phonemes
def replace(target, replacement, text):
    # Replace the first instance of a word with its phonemes
    return re.sub(r'\b' + target + r'\b', replacement, text, 1)


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

    # Method to replace heteronyms in a text line to phonemes
    def replace_het(self, text):
        # Filter the text
        working_text = ft(text)
        # Tokenize
        words = self.tokenize(working_text)
        # Get pos tags
        tags = pos_tag(words)
        # Loop through words and pos tags
        for word, pos in tags:
            # Skip if word not in dictionary
            if not self.dict.contains(word):
                continue
            # Get phonemes
            phonemes = self.dict.get_phoneme(word, pos)
            # Format phonemes
            f_ph = format_phonemes(phonemes)
            # Replace word with phonemes
            text = replace(word, f_ph, text)
        return text
