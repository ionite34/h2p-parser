# Extended Grapheme to Phoneme conversion using CMU Dictionary and Heteronym parsing.
from __future__ import annotations

from typing import Optional

from .h2p import H2p
from .h2p import replace_first
from . import format_ph as ph
from .dict_reader import DictReader
from .text.numbers import normalize_numbers
from .filter import filter_text


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

    def lookup(self, text: str) -> str | None:
        # noinspection GrazieInspection
        """
        Gets the CMU Dictionary entry for a word.

        :param text: Word to lookup
        :type: str
        """

        # Get the CMU Dictionary entry for the word
        return self.dict.get(text.lower())

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
                    elif ur_mode == 'remove':
                        text = replace_first(word, '', text)
                        continue
                    else:
                        continue
                else:
                    # Do replace
                    f_ph = ph.with_cb(ph.to_sds(entry))
                    text = replace_first(word, f_ph, text)
                    continue
            # For word in h2p dict
            else:
                # Get phonemes
                phonemes = self.h2p.dict.get_phoneme(word, pos)
                # Format phonemes
                f_ph = ph.with_cb(ph.to_sds(phonemes))
                # Replace word with phonemes
                text = replace_first(word, f_ph, text)

        # Return text
        return text
