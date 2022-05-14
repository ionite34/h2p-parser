# dictionary.py
# Defines a dictionary class that can be used to store and retrieve from the json file
from __future__ import annotations
from os.path import exists
import json
import h2p_parser.pos_parser as pos_parser
from . import DATA_PATH


# Dictionary class
class Dictionary:
    def __init__(self, file_name=None):
        # If a file name is not provided, use the default file name
        self.file_name = file_name
        if self.file_name is None:
            self.file_name = 'dict.json'
        self.dictionary = {}
        self.dictionary = self.load_dictionary(file_name)

    # Loads the dictionary from the json file
    def load_dictionary(self, path=None) -> dict:
        if path is None:
            path = DATA_PATH.joinpath(self.file_name)
        if not exists(path):
            raise FileNotFoundError(f'Dictionary {self.file_name} file not found')
        with open(str(path)) as file:
            try:
                read_dict = json.load(file)
            except json.decoder.JSONDecodeError:
                raise ValueError(f'Dictionary {self.file_name} file is not valid JSON')
        # Check dictionary has at least one entry
        if len(read_dict) == 0:
            raise ValueError('Dictionary is empty or invalid')
        return read_dict

    # Check if a word is in the dictionary
    def contains(self, word):
        word = word.lower()
        return word in self.dictionary

    # Get the phonetic pronunciation of a word using Part of Speech tag
    def get_phoneme(self, word, pos) -> str | None:
        # Get the sub-dictionary at dictionary[word]
        sub_dict = self.dictionary[word.lower()]

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

        # If no matches, return None
        return None
