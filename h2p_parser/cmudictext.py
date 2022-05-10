# Extended Grapheme to Phoneme conversion using CMU Dictionary and Heteronym parsing.
from __future__ import annotations
import re
from copy import deepcopy

import pywordsegment
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer

from .h2p import H2p
from .h2p import replace_first
from . import format_ph as ph
from .dict_reader import DictReader
from .text.numbers import normalize_numbers
from .filter import filter_text
from .processors import Processor
from .dict_cache import DictCache

re_digit = re.compile(r"\((\d+)\)")
re_bracket_with_digit = re.compile(r"\(.*\)")

# Check that the nltk data is downloaded, if not, download it
try:
    nltk.data.find('corpora/wordnet.zip')
    nltk.data.find('corpora/omw-1.4.zip')
except LookupError:
    nltk.download('wordnet')
    nltk.download('omw-1.4')


class CMUDictExt:
    def __init__(self, ph_format: str = 'sds_b', cmu_dict_path: str = None, h2p_dict_path: str = None,
                 cmu_multi_mode: int = 0, process_numbers: bool = True, phoneme_brackets: bool = True,
                 unresolved_mode: str = 'keep'):
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

        self.ph_format = ph_format
        self.cmu_dict_path = cmu_dict_path  # Path to CMU dictionary file (.txt), if None, uses built-in
        self.h2p_dict_path = h2p_dict_path  # Path to Custom H2p dictionary (.json), if None, uses built-in
        self.cmu_multi_mode = cmu_multi_mode  # CMU multi-entry resolution mode
        self.process_numbers = process_numbers  # Normalize numbers to text form, if enabled
        self.phoneme_brackets = phoneme_brackets  # If True, phonemes are wrapped in curly brackets.
        self.dict = DictReader(self.cmu_dict_path).dict  # CMU Dictionary
        self.h2p = H2p(self.h2p_dict_path, preload=True)  # H2p parser
        self.lemmatize = WordNetLemmatizer().lemmatize  # WordNet Lemmatizer - used to find singular form
        self.stem = SnowballStemmer('english').stem  # Snowball Stemmer - used to find stem root of words
        self.segment = pywordsegment.WordSegmenter().segment  # Word Segmenter
        self.p = Processor(self)  # Processor for processing text
        self.cache = DictCache()  # Cache for storing processed text

        # Features
        # Auto pluralization and de-pluralization
        self.ft_auto_plural = True
        # Auto splits and infers possessive forms of original words
        self.ft_auto_pos = True
        # Auto splits 'll
        self.ft_auto_ll = True
        # Auto splits and infers hyphenated words
        self.ft_auto_hyphenated = True
        # Auto splits possible compound words
        self.ft_auto_compound = True
        # Analyzes word root stem and infers pronunciation separately
        # i.e. 'generously' -> 'generous' + 'ly'
        self.ft_stem = True
        # Forces compound words using manual lookup
        self.ft_auto_compound_l2 = False

    def format_as(self, in_phoneme, override_format=None):
        cur_form = self.ph_format
        if override_format is not None:
            cur_form = override_format
        if cur_form == 'sds':
            output = ph.to_sds(in_phoneme)
        elif cur_form == 'sds_b':
            output = ph.with_cb(ph.to_sds(in_phoneme))
        elif cur_form == 'list':
            output = ph.to_list(in_phoneme)
        else:
            raise ValueError(f'Invalid value for ph_format: {cur_form}')
        return output

    def lookup(self, text: str, pos: str = None, cache: bool = True, ph_format=None) -> str | list | None:
        # noinspection GrazieInspection
        """
        Gets the CMU Dictionary entry for a word.

        Options for ph_format:

        - 'sds' space delimited string
        - 'sds_b' space delimited string with curly brackets
        - 'list' list of phoneme strings

        :param cache: If True, uses a cache to speed up lookups.
        :param pos: Part of speech tag (Optional)
        :param ph_format: Format of the phonemes to return:
        :type: str
        :param text: Word to lookup
        :type: str
        """

        # Get the CMU Dictionary entry for the word
        word = text.lower()
        entry = deepcopy(self.dict.get(word))  # Ensure safe copy of entry

        # Has entry, return it directly
        if entry is not None:
            return self.format_as(entry, ph_format)

        # Check if cache has the entry
        if cache:
            entry = self.cache.get(word)
            if entry is not None:
                # Check the feature source and increment the feature count
                if entry[1] is not None:
                    # Remove the leading 'auto_' from the feature name
                    feature = entry[1][5:]
                    self.p.stat_hits[feature] += 1
                    self.p.stat_resolves[feature] += 1
                return self.format_as(entry[0], ph_format)

        # Auto Possessive Processor
        if self.ft_auto_pos:
            res = self.p.auto_possessives(word)
            if res is not None:
                res = self.format_as(res, ph_format)
                # Add to cache
                if cache:
                    self.cache.add(word, res, 'auto_possessives')
                return res

        # Auto Contractions for "ll" or "d"
        if self.ft_auto_ll:
            res = self.p.auto_contractions(word)
            if res is not None:
                res = self.format_as(res, ph_format)
                # Add to cache
                if cache:
                    self.cache.add(word, res, 'auto_contractions')
                return res

        # Check for hyphenated words
        if self.ft_auto_hyphenated:
            res = self.p.auto_hyphenated(word)
            if res is not None:
                res = self.format_as(res, ph_format)
                if cache:
                    self.cache.add(word, res, 'auto_hyphenated')
                return res

        # Check for compound words
        if self.ft_auto_compound:
            res = self.p.auto_compound(word)
            if res is not None:
                res = self.format_as(res, ph_format)
                # Add to cache
                if cache:
                    self.cache.add(word, res, 'auto_compound')
                return res

        # No entry, detect if this is a multi-word entry
        if '(' in word and ')' in word and any(char.isdigit() for char in word):
            # Parse the integer from the word using regex
            num = int(re.findall(re_digit, word)[0])
            # If found
            if num is not None:
                # Remove the integer and bracket from the word
                actual_word = re.sub(re_bracket_with_digit, "", word)
                # See if this is a valid entry
                result = deepcopy(self.dict.get(actual_word))  # Ensure safe copy of entry
                # If found:
                if result is not None:
                    # Translate the integer to index
                    index = min(num - 1, 0)
                    # Check if index is less than the number of pronunciations
                    if index < len(result):
                        # Return the entry using the provided num index
                        return self.format_as(result[index], ph_format)
                    # If entry is higher
                    else:
                        # Return the highest available entry
                        return self.format_as(result[-1], ph_format)

        # Auto de-pluralization
        # This is placed near the end because we need to do a pos-tag process
        if self.ft_auto_plural:
            res = self.p.auto_plural(word, pos)
            if res is not None:
                res = self.format_as(res, ph_format)
                # Add to cache
                if cache:
                    self.cache.add(word, res, 'auto_plural')
                return res

        # Stem check
        # noinspection SpellCheckingInspection
        """
        Supported modes for words ending in:
        "ing", "ingly", "ly"
        """
        if self.ft_stem:
            res = self.p.auto_stem(word)
            if res is not None:
                res = self.format_as(res, ph_format)
                # Add to cache
                if cache:
                    self.cache.add(word, res, 'auto_stem')
                return res

        # Force compounding
        if self.ft_auto_compound_l2:
            res = self.p.auto_compound_l2(word)
            if res is not None:
                res = self.format_as(res, ph_format)
                # Add to cache
                if cache:
                    self.cache.add(word, res, 'auto_compound_l2')
                return res

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
        f_text = filter_text(text, preserve_case=True)
        words = self.h2p.tokenize(f_text)
        # Run POS tagging
        tags = self.h2p.get_tags(words)

        # Loop through words and pos tags
        for word, pos in tags:
            # Skip punctuation
            if word == '.':
                continue
            # If word not in h2p dict, check CMU dict
            if word not in self.h2p.dict:
                entry = self.lookup(word, pos)
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
