# dictionary.py

# Defines a dictionary class that can be used to store and retrieve from the json file

from os.path import exists
import importlib.resources
import json
import pos_parser


# Dictionary class
class Dictionary:
    def __init__(self, file_name=None):
        # If a file name is not provided, use the default file name
        self.file_name = file_name
        self.use_default = False
        if file_name is None:
            self.file_name = 'dict.json'
            self.use_default = True
        self.dictionary = {}
        self.load_dictionary()

    # Loads the dictionary from the json file
    def load_dictionary(self):
        if self.use_default:
            # If the file does not exist, throw an error
            if importlib.resources.path(__package__, self.file_name) is None:
                raise FileNotFoundError(f'Default Dictionary {self.file_name} file not found')
            with importlib.resources.path(__package__, self.file_name) as path:
                with open(path) as file:
                    self.dictionary = json.load(file)
        else:
            # If the file does not exist, throw an error
            if not exists(self.file_name):
                raise FileNotFoundError(f'Dictionary {self.file_name} file not found')
            with open(self.file_name) as file:
                self.dictionary = json.load(file)
        # Check dictionary has at least one entry
        if len(self.dictionary) == 0:
            raise ValueError('Dictionary is empty or invalid')

    # Check if a word is in the dictionary
    def contains(self, word):
        word = word.lower()
        return word in self.dictionary

    # Get the phonetic pronunciation of a word using Part of Speech tag
    def get_phoneme(self, word, pos):
        # Get the sub-dictionary at dictionary[word]
        sub_dict = self.dictionary[word]

        # First, check if the exact pos is a key
        if pos in sub_dict:
            return sub_dict[pos]

        # If not, use the parent pos of the pos tag
        parent_pos = pos_parser.get_parent_pos(pos)

        if parent_pos is not None:
            # Check if the sub_dict contains the parent pos
            if parent_pos in sub_dict:
                return sub_dict[parent_pos]

        # If not, check if the sub_dict contains a DEFAULT key
        if 'DEFAULT' in sub_dict:
            return sub_dict['DEFAULT']
        else:
            # If no default, return None
            return None
