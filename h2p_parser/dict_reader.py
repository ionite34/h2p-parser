# This reads a CMUDict formatted dictionary as a dictionary object
import re


def read_dict(filename):
    with open(filename, encoding='utf-8', mode='r') as f:
        # Read the file into lines
        lines = f.readlines()
        # Remove trailing whitespaces
        for line in lines:
            line = line.rstrip()
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

        word = pairs[0]
        phonemes = pairs[1:]
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


class DictReader:
    def __init__(self, filename):
        self.filename = filename
        self.dictionary = {}
        self.dictionary = read_dict(filename)
