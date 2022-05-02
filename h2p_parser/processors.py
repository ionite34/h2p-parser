# Transformations of text sequences for matching
from __future__ import annotations
from typing import TYPE_CHECKING

import re

if TYPE_CHECKING:
    from .cmudictext import CMUDictExt

_re_digit = re.compile(r'\d+')


class Processor:
    def __init__(self, cde: CMUDictExt):
        self._lookup = cde.lookup
        # Number of times respective methods were called
        self.stat_hits = {
            'plural': 0,
            'possessives': 0,
            'contractions': 0,
            'hyphenated': 0,
            'compound': 0,
            'stem': 0
        }
        # Number of times respective methods returned value (not None)
        self.stat_resolves = {
            'plural': 0,
            'possessives': 0,
            'contractions': 0,
            'hyphenated': 0,
            'compound': 0,
            'stem': 0
        }
        # Holds events when features encountered unexpected language syntax
        self.stat_unexpected = {
            'plural': [],
            'possessives': [],
            'contractions': [],
            'hyphenated': [],
            'compound': [],
            'stem': []
        }

    def auto_possessives(self, word: str) -> str | None:
        """
        Auto-possessives
        :param word: Input of possible possessive word
        :return: Phoneme of word as SDS, or None if unresolvable
        """
        if not word.endswith("'s"):
            return None
        # If the word ends with "'s", register a hit
        self.stat_hits['possessives'] += 1
        """
        There are 3 general cases:
        1. Base words ending in one of 6 special consonants (sibilants)
            - i.e. Tess's, Rose's, Butch's, Midge's, Rush's, Garage's
            - With consonants ending of [s], [z], [ch], [j], [sh], [zh]
            - In ARPAbet: {S}, {Z}, {CH}, {JH}, {SH}, {ZH}
            - These require a suffix of {IH0 Z}
        2. Base words ending in vowels and voiced consonants:
            - i.e. Fay's, Hugh's, Bob's, Ted's, Meg's, Sam's, Dean's, Claire's, Paul's, Bing's
            - In ARPAbet: {IY0}, {EY1}, {UW1}, {B}, {D}, {G}, {M}, {N}, {R}, {L}, {NG}
            - Vowels need a wildcard match of any numbered variant
            - These require a suffix of {Z}
        3. Base words ending in voiceless consonants:
            - i.e. Hope's, Pat's, Clark's, Ruth's
            - In ARPAbet: {P}, {T}, {K}, {TH}
            - These require a suffix of {S}
        """

        # Method to return phoneme and increment stat
        def _resolve(phoneme: str) -> str:
            self.stat_resolves['possessives'] += 1
            return phoneme

        word = word[:-2]  # Get core word without possessive
        entry = self._lookup(word, ph_format='sds')  # find core word using recursive search
        if entry is None:
            return None  # Core word not found

        ph = entry[0]  # get the inner phoneme
        # [Case 1]
        if ph[-1] in {'S', 'Z', 'CH', 'JH', 'SH', 'ZH'}:
            ph += 'IH0' + 'Z'
            return _resolve(ph)
        # [Case 2]
        """
        Valid for case 2:
        'AA', 'AO', 'EY', 'OW', 'UW', 'AE', 'AW', 'EH', 'IH', 
        'OY', 'AH', 'AY', 'ER', 'IY', 'UH', 'UH', 
        'B', 'D', 'G', 'M', 'N', 'R', 'L', 'NG'
        To simplify matching, we will check for the listed single-letter variants and 'NG'
        and then check for any numbered variant
        """
        if ph[-1] in {'B', 'D', 'G', 'M', 'N', 'R', 'L', 'NG'} or ph[-1:][-1:].isdigit():
            ph += 'Z'
            return _resolve(ph)
        # [Case 3]
        if ph[-1] in ['P', 'T', 'K', 'TH']:
            ph += 'S'
            return _resolve(ph)

        return None  # No match found

    def auto_contractions(self, word: str) -> str | None:
        """
        Auto contracts form and finds phonemes
        :param word:
        :return:
        """
        """
        Supported contractions:
        - 's'
        - 've'
        - 'll'
        - 'd'
        - 're'
        """
        # First, check if the word is a contraction
        parts = word.split("\'")  # Split on [']
        if len(parts) == 1:
            return None  # No contraction found
        # If initial check passes, register a hit
        self.stat_hits['contractions'] += 1
