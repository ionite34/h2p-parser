# dictionary.py

# Defines a dictionary class that can be used to store and retrieve from the json file

import importlib.resources
import json


# Dictionary class
class Dictionary:
    def __init__(self, file_name=None):
        # If a file name is not provided, use the default file name
        if file_name is None:
            self.file_name = 'dict.json'
            self.use_default = True
        self.file_name = file_name
        self.dictionary = {}
        self.load_dictionary()

    # Loads the dictionary from the json file
    def load_dictionary(self):
        if self.use_default:
            with importlib.resources.path(__package__, self.file_name) as path:
                with open(path) as file:
                    self.dictionary = json.load(file)
        else:
            with open(self.file_name) as file:
                self.dictionary = json.load(file)

    # Check if a word is in the dictionary
    def is_word(self, word):
        return word in self.dictionary

    # Get the phonetic pronunciation of a word using Part of Speech tag
    def get_phoneme(self, word, pos):
        # Get the sub-dictionary at dictionary[word]
        sub_dict = self.dictionary[word]
        # First, check if the exact pos is a key
        if pos in sub_dict:
            return sub_dict[pos]
        # If not,
        return self.dictionary[word][pos]
