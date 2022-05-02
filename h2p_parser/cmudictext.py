# Extended Grapheme to Phoneme conversion using CMU Dictionary and Heteronym parsing.
from __future__ import annotations

import re
from typing import Optional

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
        self.h2p = H2p(self.h2p_dict_path, preload=True)  # H2p parser
        self.lemmatize = WordNetLemmatizer().lemmatize  # WordNet Lemmatizer - used to find singular form
        self.stem = SnowballStemmer('english').stem  # Snowball Stemmer - used to find stem root of words
        self.p = Processor(self)  # Processor for processing text

        # Features
        self.segment = pywordsegment.WordSegmenter().segment
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

        # Holds number stats on feature usage
        self.ft_stats = {
            'plural': 0,
            'pos': 0,
            'hyphenated': 0,
            'compound': 0,
            'stem': 0,
            'll': 0,
        }

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

        def format_as(in_phoneme):
            if ph_format == 'sds':
                output = ph.to_sds(in_phoneme)
            elif ph_format == 'sds_b':
                output = ph.with_cb(ph.to_sds(in_phoneme))
            elif ph_format == 'list':
                output = ph.to_list(in_phoneme)
            else:
                raise ValueError('Invalid value for ph_format: {}'.format(ph_format))
            return output

        # Get the CMU Dictionary entry for the word
        word = text.lower()
        entry = self.dict.get(word)

        # Has entry, return it directly
        if entry is not None:
            return format_as(entry)

        # Auto Possessive Processor
        if self.ft_auto_pos:
            res = self.p.auto_possessives(word)
            if res is not None:
                return format_as(res)

        # For word ending with "'ll" or "'d"
        if self.ft_auto_ll and word.endswith("'ll"):
            word = word[:-3]  # Get core word without possessive
            entry = self.dict.get(word)  # find core word
            if entry is not None:  # if core word exists
                phoneme = entry[0]  # get the inner phoneme
                # Add 'L' to the end of the phoneme
                phoneme += 'L'
                # Increment feature usage stats
                self.ft_stats['ll'] += 1
                return format_as(phoneme)

        # Check for possible compound words
        if self.ft_auto_compound:
            split = self.segment(word)
            # If match
            if len(split) > 1:
                # Recursively lookup each part
                all_exists = True
                for part in split:
                    part_ph = self.lookup(part, ph_format=ph_format)
                    if part_ph is None:
                        all_exists = False
                # If all parts exist, return the compound
                if all_exists:
                    self.ft_stats['compound'] += 1  # Increment feature usage stats
                    return format_as(' '.join(self.lookup(part, ph_format='sds') for part in split))

        # CHeck for hyphenated words
        if self.ft_auto_hyphenated and '-' in word:
            # Split the word into two parts
            split = word.split('-')
            # Lookup each part
            all_exists = True
            for part in split:
                part_ph = self.lookup(part, ph_format=ph_format)
                if part_ph is None:
                    all_exists = False
            # If all parts exist, return the compound
            if all_exists:
                self.ft_stats['hyphenated'] += 1  # Increment feature usage stats
                return format_as(' '.join(self.lookup(part, ph_format='sds') for part in split))

        # No entry, detect if this is a multi-word entry
        if '(' in word and ')' in word and any(char.isdigit() for char in word):
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
                    # Translate the integer to index
                    index = min(num - 1, 0)
                    # Check if index is less than the number of pronunciations
                    if index < len(result):
                        # Return the entry using the provided num index
                        return format_as(result[index])
                    # If entry is higher
                    else:
                        # Return the highest available entry
                        return format_as(result[-1])

        # Auto de-pluralization
        # This is placed near the end because we need to do a pos-tag process
        if self.ft_auto_plural:
            # Do tag
            tag = self.h2p.tag(word)
            # Check if tag valid
            if tag is not None and len(tag) > 0:
                # If tag is a plural noun or plural proper noun
                if tag[0] == 'NNS' or tag[0] == 'NNPS':
                    # Get singular form using lemmatization
                    singular = self.lemmatize(word, 'n')
                    # First check if the singular is in the dictionary, if not there's no point to continue
                    if self.dict.get(singular) is not None:
                        # If singular ends in 's', 'ss', 'sh', 'ch', 'x', or 'z', add 'es' to predict the plural
                        if len(singular) > 2 and (singular[-2] in ['ss', 'sh', 'ch'] or singular[-1] in ['s', 'x', 'z']):
                            predicted_plural = singular + 'es'
                            # If match
                            if word == predicted_plural:
                                # Recursively lookup the singular
                                ph_singular = self.lookup(singular, ph_format='sds')
                                ph_es = 'AH0 Z'
                                self.ft_stats['plural'] += 1  # Increment feature usage stats
                                return format_as(' '.join([ph_singular, ph_es]))
                        else:
                            # Otherwise, predict by just adding 's'
                            predicted_plural = singular + 's'
                            # If match
                            if word == predicted_plural:
                                # Recursively lookup the singular
                                ph_singular = self.lookup(singular, ph_format='sds')
                                ph_s = 'Z'
                                self.ft_stats['plural'] += 1  # Increment feature usage stats
                                return format_as(' '.join([ph_singular, ph_s]))

        # Stem check
        # noinspection SpellCheckingInspection
        """
        Supported modes for words ending in:
        "ing", "ingly", "ly"
        """
        if self.ft_stem:
            if word.endswith('ing'):
                # Check if the base word is in the dictionary
                if self.dict.get(word[:-3]) is not None:
                    # Verify stem is valid
                    if self.stem(word) == word[:-3]:
                        # Recursively join the root and 'ing'
                        ph_root = self.lookup(word[:-3], ph_format='sds')
                        ph_ing = 'IH0 NG'
                        self.ft_stats['stem'] += 1  # Increment feature usage stats
                        return format_as(' '.join([ph_root, ph_ing]))
            elif word.endswith('ingly'):
                # Check if the base word is in the dictionary
                if self.dict.get(word[:-5]) is not None:
                    # Verify stem is valid
                    if self.stem(word) == word[:-5]:
                        # Recursively join the root and 'ingly'
                        ph_root = self.lookup(word[:-5], ph_format='sds')
                        ph_ingly = 'IH0 NG L IY0'
                        self.ft_stats['stem'] += 1  # Increment feature usage stats
                        return format_as(' '.join([ph_root, ph_ingly]))
            elif word.endswith('ly'):
                # Check if the base word is in the dictionary
                if self.dict.get(word[:-2]) is not None:
                    # Verify stem is valid
                    if self.stem(word) == word[:-2]:
                        # Recursively join the root and 'ly'
                        ph_root = self.lookup(word[:-2], ph_format='sds')
                        ph_ly = 'L IY0'
                        self.ft_stats['stem'] += 1  # Increment feature usage stats
                        return format_as(' '.join([ph_root, ph_ly]))

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
