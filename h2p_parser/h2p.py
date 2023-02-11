from __future__ import annotations
import nltk
import re
from nltk.tokenize import TweetTokenizer
from nltk import pos_tag
from nltk import pos_tag_sents
from .dictionary import Dictionary
from .filter import filter_text as ft
from .format_ph import to_sds, with_cb

# Check that the nltk data is downloaded, if not, download it
try:
    nltk.data.find('taggers/averaged_perceptron_tagger.zip')
except LookupError:
    nltk.download('averaged_perceptron_tagger')


# Method to use Regex to replace the first instance of a word with its phonemes
def replace_first(target, replacement, text):
    # Skip if target invalid
    if target is None or target == '':
        return text
    # Replace the first instance of a word with its phonemes
    return re.sub(r'(?i)\b' + re.escape(target) + r'\b', replacement, text, 1)


class H2p:
    def __init__(self, dict_path=None, preload=False, phoneme_format=None):
        """
        H2p Parser

        Supported phoneme formats:
            - [sds] Space delimited
            - [sds_cb] (Default) Space delimited surrounded by { }

        :param dict_path: Path to a heteronym dictionary json file. Built-in dictionary will be used if None
        :type dict_path: str
        :param preload: Preloads the tokenizer and tagger during initialization
        :type preload: bool
        """

        # Supported phoneme formats
        if phoneme_format not in [None, 'sds', 'sds_cb']:
            raise ValueError('Phoneme format must be one of: sds, sds_cb')
        if phoneme_format is None:
            self._ph_format = 'sds_cb'
        else:
            self._ph_format = phoneme_format
        # Load format
        if self._ph_format == 'sds':
            self.format = to_sds
        elif self._ph_format == 'sds_cb':
            self.format = lambda a: with_cb(to_sds(a))
        self.dict = Dictionary(dict_path)
        self.tokenize = TweetTokenizer().tokenize
        self.get_tags = pos_tag
        if preload:
            self.preload()

    def preload(self) -> None:
        """
        Preloads the tokenizer and tagger
        :return: None
        """
        tokens = self.tokenize('a')
        assert tokens == ['a']
        assert pos_tag(tokens)[0][0] == 'a'

    def contains_het(self, text: str) -> bool:
        """
        Checks if a text line contains a heteronym
        :param text: Text line to check
        :return: True if contains a heteronym, False otherwise
        """
        # Filter the text
        text = ft(text)
        # Tokenize
        words = self.tokenize(text)
        # Check match with dictionary
        for word in words:
            if self.dict.contains(word):
                return True
        return False

    def replace_het(self, text: str) -> str:
        """
        Replaces heteronyms in a text line with phonemes
        :param text: Text to replace heteronyms in
        :return: Text with heteronyms replaced with phonemes
        """
        # Filter the text
        working_text = ft(text, preserve_case=True)
        # Tokenize
        words = self.tokenize(working_text)
        # Get pos tags
        tags = pos_tag(words)
        # Loop through words and pos tags
        for word, pos in tags:
            # Skip if word not in dictionary
            if not str(word).isalpha() or not self.dict.contains(word):
                continue
            # Get phonemes
            phonemes = self.dict.get_phoneme(word, pos)
            # Format phonemes
            f_ph = self.format(phonemes)
            # Replace word with phonemes
            text = replace_first(word, f_ph, text)
        return text

    def replace_het_list(self, text_list: list[str]) -> list[str]:
        """
        Replaces heteronyms in a list of text lines
        :param text_list: List of text lines
        :return: List of text lines with heteronyms replaced
        """
        # Filter the text
        working_text_list = [ft(text, preserve_case=True) for text in text_list]
        # Tokenize
        list_sentence_words = [self.tokenize(text) for text in working_text_list]
        # Get pos tags list
        tags_list = pos_tag_sents(list_sentence_words)
        # Loop through lines
        for index in range(len(tags_list)):
            # Loop through words and pos tags in tags_list index
            for word, pos in tags_list[index]:
                # Skip if word not in dictionary
                if not self.dict.contains(word):
                    continue
                # Get phonemes
                phonemes = self.dict.get_phoneme(word, pos)
                # Format phonemes
                f_ph = self.format(phonemes)
                # Replace word with phonemes
                text_list[index] = replace_first(word, f_ph, text_list[index])
        return text_list

    def tag(self, text: str) -> list[str]:
        """
        Tags a text line
        :param text: Text line to tag
        :return: List of tags
        """
        # Filter the text
        working_text = ft(text, preserve_case=True)
        # Tokenize
        words = self.tokenize(working_text)
        # Get pos tags
        tags = pos_tag(words)
        # Only return element 1 of each list
        return [tag[1] for tag in tags]

