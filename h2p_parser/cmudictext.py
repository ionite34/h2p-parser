# Extended Grapheme to Phoneme conversion using CMU Dictionary and Heteronym parsing.
from __future__ import annotations

import re
from typing import Optional

from .h2p import H2p
from .h2p import replace_first
from . import format_ph as ph
from .dict_reader import DictReader
from .text.numbers import normalize_numbers
from .filter import filter_text

re_digit = re.compile(r"\((\d+)\)")
re_bracket_with_digit = re.compile(r"\(.*\)")


class CMUDictExt:
    def __init__(self, cmu_dict_path: str = None, h2p_dict_path: str = None, cmu_multi_mode: int = 0,
                 process_numbers: bool = True, phoneme_brackets: bool = True, unresolved_mode: str = 'keep'):
        # noinspection GrazieInspection
        """
        Initialize CMUDictExt - Extended Grapheme to Phoneme conversion using CMU Dictionary with Heteronym parsing.

        CMU multi-entry resolution modes:
            - -2 : Raw entry (i.e. 'A' resolves to 'AH0' and 'A(1)' to 'EY1')
            - -1 : Skip resolving any entry with multiple pronunciations.
            - 0 : Resolve using default un-numbered pronunciation.
            - 1 : Resolve using (1) numbered pronunciation.
            - n : Resolve using (n) numbered pronunciation.
            - If a higher number is specified than available for the word, the highest available number is used.

        Unresolved word resolution modes:
            - keep : Keep the text-form word in the output.
            - remove : Remove the text-form word from the output.
            - drop : Return the line as None if any word is unresolved.

        :param cmu_dict_path: Path to CMU dictionary file (.txt)
        :type: str
        :param h2p_dict_path: Path to Custom H2p dictionary (.json)
        :type: str
        :param cmu_multi_mode: CMU resolution mode for entries with multiple pronunciations.
        :type: int
        """

        # Check valid unresolved_mode argument
        if unresolved_mode not in ['keep', 'remove', 'drop']:
            raise ValueError('Invalid value for unresolved_mode: {}'.format(unresolved_mode))
        self.unresolved_mode = unresolved_mode

        self.cmu_dict_path = cmu_dict_path  # Path to CMU dictionary file (.txt), if None, uses built-in
        self.h2p_dict_path = h2p_dict_path  # Path to Custom H2p dictionary (.json), if None, uses built-in
        self.cmu_multi_mode = cmu_multi_mode  # CMU multi-entry resolution mode
        self.process_numbers = process_numbers  # Normalize numbers to text form, if enabled
        self.phoneme_brackets = phoneme_brackets  # If True, phonemes are wrapped in curly brackets.
        self.dict = DictReader(self.cmu_dict_path).dict  # CMU Dictionary
        self.h2p = H2p(self.h2p_dict_path, preload=True)

    def lookup(self, text: str, ph_format: str = 'sds') -> str | list | None:
        # noinspection GrazieInspection
        """
        Gets the CMU Dictionary entry for a word.

        Options for ph_format:

        - 'sds' space delimited string
        - 'sds_b' space delimited string with curly brackets
        - 'list' list of phoneme strings

        :param ph_format: Format of the phonemes to return:
        :type: str
        :param text: Word to lookup
        :type: str
        """

        def format_as(phoneme):
            if ph_format == 'sds':
                output = ph.to_sds(phoneme)
            elif ph_format == 'sds_b':
                output = ph.to_sds(phoneme)
                output = '{' + output + '}'
            elif ph_format == 'list':
                output = ph.to_list(phoneme)
            else:
                raise ValueError('Invalid value for ph_format: {}'.format(ph_format))
            return output

        # Get the CMU Dictionary entry for the word
        word = text.lower()

        # Has entry, return it
        entry = self.dict.get(word)
        if entry is not None:
            return format_as(entry)

        # No entry, detect if this is a multi-word entry
        if ('(' in word) and (')' in word) and any(char.isdigit() for char in word):
            # Parse the integer from the word using regex
            num = int(re.findall(re_digit, word)[0])
            # If found
            if num is not None:
                # Remove the integer and bracket from the word
                actual_word = re.sub(re_bracket_with_digit, "", word)
                # See if this is a valid entry
                result = self.dict.get(actual_word)
                # If found:
                if result is not None:
                    # Check if the provided num is equal or less than the number of pronunciations
                    if num < len(result):
                        # Return the entry using the provided num index
                        return format_as(result[num])
                    # If entry is higher
                    else:
                        # Return the highest available entry
                        return format_as(result[-1])
        # If not found
        return None

    def convert(self, text: str) -> str | None:
        # noinspection GrazieInspection
        """
        Replace a grapheme text line with phonemes.

        :param text: Text line to be converted
        :type: str
        """

        # Check valid unresolved_mode argument
        if self.unresolved_mode not in ['keep', 'remove', 'drop']:
            raise ValueError('Invalid value for unresolved_mode: {}'.format(self.unresolved_mode))
        ur_mode = self.unresolved_mode

        # Normalize numbers, if enabled
        if self.process_numbers:
            text = normalize_numbers(text)
        # Filter and Tokenize
        f_text = filter_text(text)
        words = self.h2p.tokenize(f_text)
        # Run POS tagging
        tags = self.h2p.get_tags(words)

        # Loop through words and pos tags
        for word, pos in tags:
            # Skip punctuation
            if word == '.':
                continue
            # If word not in h2p dict, check CMU dict
            if not self.h2p.dict.contains(word):
                entry = self.lookup(word)
                if entry is None:
                    if ur_mode == 'drop':
                        return None
                    if ur_mode == 'remove':
                        text = replace_first(word, '', text)
                    continue
                # Do replace
                f_ph = ph.with_cb(ph.to_sds(entry))
                text = replace_first(word, f_ph, text)
                continue
            # For word in h2p dict, get phonemes
            phonemes = self.h2p.dict.get_phoneme(word, pos)
            # Format phonemes
            f_ph = ph.with_cb(ph.to_sds(phonemes))
            # Replace word with phonemes
            text = replace_first(word, f_ph, text)
        # Return text
        return text
