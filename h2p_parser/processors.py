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
        self._segment = cde.segment
        self._tag = cde.h2p.tag
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
        - 'll
        - 'd
        """
        # First, check if the word is a contraction
        parts = word.split("\'")  # Split on [']
        if len(parts) == 1 or parts[1] not in {'ll', 'd'}:
            return None  # No contraction found
        if len(parts) > 2:
            self.stat_unexpected['contraction'] += word
            return None  # More than 2 parts, can't be a contraction
        # If initial check passes, register a hit
        self.stat_hits['contractions'] += 1

        # Get the core word
        core = parts[0]
        # Get the phoneme for the core word recursively
        ph = self._lookup(core, ph_format='list')
        if ph is None:
            return None  # Core word not found
        # Add the phoneme with the appropriate suffix
        if parts[1] == 'll':
            ph += 'L'
        elif parts[1] == 'd':
            ph += 'D'
        # Return the phoneme
        self.stat_resolves['contractions'] += 1
        return ph

    def auto_hyphenated(self, word: str) -> str | None:
        """
        Splits hyphenated words and attempts to resolve components
        :param word:
        :return:
        """
        # First, check if the word is a hyphenated word
        if '-' not in word:
            return None  # No hyphen found
        # If initial check passes, register a hit
        self.stat_hits['hyphen'] += 1
        # Split the word into parts
        parts = word.split('-')
        # Get the phonemes for each part
        ph = []
        for part in parts:
            ph_part = self._lookup(part, ph_format='sds')
            if ph_part is None:
                return None  # Part not found
            ph.append(ph_part)
        # Join the phonemes
        ph = ' '.join(ph)
        # Return the phoneme
        self.stat_resolves['hyphenated'] += 1
        return ph

    def auto_compound(self, word: str) -> str | None:
        """
        Splits compound words and attempts to resolve components
        :param word:
        :return:
        """
        # Split word into parts
        parts = self._segment(word)
        if len(parts) == 1:
            return None  # No compound found
        # If initial check passes, register a hit
        self.stat_hits['compound'] += 1
        # Get the phonemes for each part
        ph = []
        for part in parts:
            ph_part = self._lookup(part, ph_format='sds')
            if ph_part is None:
                return None  # Part not found
            ph.append(ph_part)
        # Join the phonemes
        ph = ' '.join(ph)
        # Return the phoneme
        self.stat_resolves['compound'] += 1
        return ph

    def auto_plural(self, word: str) -> str | None:
        """
        Finds singular form of plurals and attempts to resolve seperately
        :param word:
        :return:
        """
        # First, check if the word is a replaceable plural
        # Needs to end in 's' or 'es'
        if word[-1] != 's':
            return None  # No plural found
        # Now check if the word is a plural using pos
        tag = self._tag(word)
        if tag is None or len(tag) == 0 or tag[0] != 'NNS' or tag[0] != 'NNPS':
            return None  # No tag found
        # If initial check passes, register a hit
        self.stat_hits['plural'] += 1
        # Get the singular form



