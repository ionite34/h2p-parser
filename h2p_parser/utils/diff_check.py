# Checks OOV words in supplied dictionary files against the built-in CMU dictionary.
import os

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
# noinspection PyProtectedMember
from InquirerPy.base.control import Separator
from InquirerPy.utils import color_print as cp
from tqdm import tqdm

from . import ui
from .. import cmudictext
from .. import format_ph as fp
from .. import dict_reader
from .ui_common import *
from .parse_line import UIParseLine


class UIDiffCheck:
    def __init__(self):
        self.cmu = dict_reader.DictReader().dict

    def execute(self):
        """
        Parses external dictionaries for OOV words from CMU dict.
        """
        # Choose Whole Directory or Single File
        mode = inquirer.select(
            message='Select mode:',
            choices=[
                "Directory",
                "File",
                Choice(value=None, name='[Back]')
            ],
            default=0,
        ).execute()
        if mode is None:
            ui.menu_tests()  # Return to tests menu

        # Select IPA / ARPAbet mode
        ipa_arp_mode = inquirer.select(
            message='Select symbol type:',
            choices=[
                "ARPAbet",
                "IPA",
                Choice(value=None, name='[Back]')
            ],
            default=0,
        ).execute()
        if mode is None:
            ui.menu_tests()  # Return to tests menu

        if ipa_arp_mode == "ARPAbet":
            convert_ipa = False
        else:
            convert_ipa = True

        # Select input based on mode
        if mode == "Directory":
            selected = prompt_d_input()
            self.run_directory(selected, convert_ipa)
            print()
            ui.menu_tests()  # Return to tests menu
        elif mode == "File":
            selected = prompt_f_input()
            self.run_file(selected)
            print()
            ui.menu_tests()  # Return to tests menu

    def run_directory(self, directory, convert_ipa: bool = False):
        # Runs diff check on all dictionaries in a directory
        # Get a list of all files in the directory
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if len(files) == 0:
            print("No files found in directory.")
            return
        # Combine the dictionaries into a single dictionary
        result = {}
        result_unmappable = {}
        for file in tqdm(files, desc='Reading files', unit='files', position=0):
            # Get full path to file
            file_path = os.path.join(directory, file)
            dr = dict_reader.DictReader(file_path)
            result_unmappable.update(dr.unmappable_words)
            result.update(dr.dict)
        # Run diff check on combined dictionary
        oov = set()  # Unique OOV words
        oov_dict = {}  # OOV words and their corresponding entries
        all_words = set()  # Unique All words
        for word in tqdm(result, desc='Checking OOV words'):
            all_words.add(word.lower())
            if word.lower() not in self.cmu:
                oov.add(word)
                oov_dict[word] = result[word]
        # Print results
        print()  # Newline
        cp([("#d21205", "Found: "), ("white", f"{len(oov)}/{len(all_words)}"),
            ("#d21205", " words not in CMU dict.")])
        # If IPA
        if convert_ipa and len(result_unmappable) > 0:
            cp([("orange", "Warning: "), ("white", f"{len(oov)}/{len(all_words)}"),
                ("orange", " words not mappable to ARPAbet from IPA.")])
        # Ask user if they'd like to list the results
        if len(result) > 0 and inquirer.confirm(
                message='Would you like to browse the OOV words?',
                default=True,
        ).execute():
            # List the OOV words by using parse_line
            UIParseLine().execute_cmu(result)

    def run_file(self, file_path):
        # Runs diff check for specified file
        # Get a list of all files in the directory
        dr = dict_reader.DictReader(file_path)
        result = dr.dict
        # Run diff check on combined dictionary
        oov = set()  # Unique OOV words
        oov_dict = {}  # OOV words and their corresponding entries
        all_words = set()  # Unique All words
        for word in tqdm(result, desc='Checking OOV words'):
            all_words.add(word.lower())
            if word.lower() not in self.cmu:
                oov.add(word)
                oov_dict[word] = result[word]
        # Print results
        print()  # Newline
        cp([("#d21205", "Found: "), ("white", f"{len(oov)}/{len(all_words)}"),
            ("#d21205", " words not in CMU dict.")])
        # Ask user if they'd like to list the results
        if len(result) > 0 and inquirer.confirm(
                message='Would you like to browse the OOV words?',
                default=True,
        ).execute():
            # List the OOV words by using parse_line
            UIParseLine().execute_cmu(oov_dict)
