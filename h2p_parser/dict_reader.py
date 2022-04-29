# This reads a CMUDict formatted dictionary as a dictionary object
import re
import h2p_parser.format_ph as ph
import nltk
from nltk.corpus import cmudict


def read_dict(filename):
    with open(filename, encoding='utf-8', mode='r') as f:
        # Read the file into lines
        lines = f.readlines()
    # Remove trailing whitespaces
    lines = [line.rstrip() for line in lines]
    return lines


def parse_dict(lines: list) -> dict:
    # Create a dictionary to store the parsed data
    parsed_dict = {}
    # Iterate over the lines
    for line in lines:
        # Skip beginning comments that begin with ";;;"
        if line.startswith(';;;') or line == '':
            continue

        # Skip if no delimiter is found
        if '  ' not in line:
            continue

        # Split the line by double space into word and phoneme pairs
        pairs = line.split('  ')

        # Skip if empty length
        if len(pairs) == 0:
            continue

        word = str.lower(pairs[0])  # Get word and lowercase it
        phonemes = ph.to_list(pairs[1])   # Convert to list of phonemes
        phonemes = [phonemes]  # Wrap in nested list
        word_num = 0
        word_orig = None

        # Detect if this is a multi-word entry
        if ('(' in word) and (')' in word) and any(char.isdigit() for char in word):
            # Parse the integer from the word using regex
            result = int(re.findall(r"\((\d+)\)", word)[0])
            # If found
            if result is not None:
                # Set the original word
                word_orig = word
                # Remove the integer and bracket from the word
                word = re.sub(r"\(.*\)", "", word)
                # Set the word number to the result
                word_num = result

        # Check existing key
        if word in parsed_dict:
            # If word number is 0, ignore
            if word_num == 0:
                continue
            # If word number is not 0, add phoneme to existing key at index
            parsed_dict[word].extend(phonemes)
            # Also add the original word if it exists
            if word_orig is not None:
                parsed_dict[word_orig] = phonemes
        else:
            # Create a new key
            parsed_dict[word] = phonemes

    # Return the dictionary
    return parsed_dict


def get_cmu_dict() -> dict:
    # Get the CMU dictionary from nltk
    # Ensure nltk data downloaded
    try:
        nltk.data.find('corpora/cmudict.zip')
    except LookupError:
        nltk.download('cmudict')
    return cmudict.dict()


class DictReader:
    def __init__(self, filename=None):
        # If filename is None, use the default dictionary (nltk)
        self.filename = filename
        self.dict = {}
        if self.filename is not None:
            self.dict = parse_dict(read_dict(self.filename))
        else:
            self.dict = get_cmu_dict()
