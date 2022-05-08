# Parses annotation files for conversion of sentences to phonemes
from __future__ import annotations

import time

from h2p_parser import cmudictext
from h2p_parser.filter import filter_text
from h2p_parser.text.numbers import normalize_numbers
from h2p_parser.symbols import punctuation

# Reads a file into a list of lines
from tqdm import tqdm


def parse_file(file_name, delimiter) -> ParseResult:
    lines = read_file(file_name, delimiter)
    result = check_lines(lines)
    return result


def read_file(file_name, delimiter) -> list:
    with open(file_name, 'r', encoding="utf-8") as f:
        result = []
        for line in f:
            line = line.split(delimiter)
            # Take the second element
            result.append(line[1].lower())
        return result


# Checks a list of lines for unresolvable words
# Returns a list of lines with unresolvable words, or None if no unresolvable words
def check_lines(lines: list) -> ParseResult:
    # Create cde
    cde = cmudictext.CMUDictExt()
    # Load database
    cde.cache.load()
    # Create result
    result = ParseResult()

    # Start timer to record time
    start_time = time.time()

    for line in tqdm(lines, desc="Parsing lines"):
        parse_line(line, result, cde)

    # Stop timer
    end_time = time.time()
    elapsed_ms = round((end_time-start_time) * 100, 2)
    ms_per_line = round((end_time-start_time) / len(lines) * 100, 2)
    us_per_line = round((end_time-start_time) / len(lines) * 100 * 1000, 2)
    print(f"[Time taken]: {elapsed_ms} ms")
    if ms_per_line < 1.0:
        print(f"[Time per line]: {us_per_line} μs")
    else:
        print(f"[Time per line]: {ms_per_line} ms")

    print()

    # Save database
    cde.cache.save()

    # Set features
    result.ft_stats = cde.p.stat_resolves
    return result


def parse_line(line: str, result: ParseResult, cde: cmudictext.CMUDictExt):
    # Add
    result.all_lines.append(line)
    result.lines.add(line)

    # Filter the line
    f_line = filter_text(line)
    # Number converter
    f_line = normalize_numbers(f_line)
    # Tokenize
    tokens = cde.h2p.tokenize(f_line)
    # Flags
    unresolvable = False
    required_het = False
    required_fet = False
    for word in tokens:
        # Skip word if punctuation
        if word in punctuation:
            continue
        # Add word to result
        result.all_words.append(word)
        result.words.add(word)
        # Check if word is resolvable
        if cde.h2p.contains_het(word):
            required_het = True
            result.n_words_res += 1
            result.n_words_het += 1
        elif cde.dict.get(word) is not None:
            result.n_words_res += 1
            result.n_words_cmu += 1
        elif cde.lookup(word) is not None:
            required_fet = True
            result.n_words_res += 1
            result.n_words_fet += 1
        else:
            unresolvable = True
            result.unres_all_words.append(word)
            result.unres_words.add(word)

    if required_het:
        result.all_lines_cont_het.append(line)

    if required_fet:
        result.all_lines_cont_fet.append(line)

    if not required_fet and required_het and not unresolvable:
        result.all_lines_only_cmu_h2p.append(line)

    if not required_het and not required_fet and not unresolvable:
        result.all_lines_only_cmu.append(line)

    if unresolvable:
        result.unres_all_lines.append(line)
        result.unres_lines.add(line)


# Class to hold the result of a parse
class ParseResult:
    def __init__(self):
        self.all_lines = []
        self.all_lines_cont_het = []
        self.all_lines_cont_fet = []
        self.all_lines_only_cmu = []
        self.all_lines_only_cmu_h2p = []
        self.unres_all_lines = []
        self.lines = set()
        self.unres_lines = set()
        # Words
        self.all_words = []
        self.unres_all_words = []
        self.words = set()
        self.unres_words = set()
        # Numerical stats
        self.n_words_res = 0  # Number of total resolved words
        self.n_words_cmu = 0  # Resolved words from CMU
        self.n_words_fet = 0  # Resolved words from Features
        self.n_words_het = 0  # Resolved words from H2p
        # Stats from cmudictext
        self.ft_stats = None

    # Get lines resolved
    def get_lines_res(self):
        # This is all lines - unresolved lines
        return len(self.all_lines) - len(self.unres_all_lines)

    # Get lines covered with CMUDict + H2p only
    def get_lines_cmu_h2p(self):
        # All resolved lines
        all_res = len(self.all_lines) - len(self.unres_all_lines)
        # Remove lines containing features
        cmu_h2p_res = all_res - len(self.all_lines_cont_fet)
        return cmu_h2p_res

    # Get percentage of lines covered
    def line_unique_coverage(self) -> float:
        dec = 1 - len(self.unres_lines) / len(self.lines)
        return round(dec * 100, 2)

    # Get percentage of words covered
    def word_unique_coverage(self) -> float:
        dec = 1 - len(self.unres_words) / len(self.words)
        return round(dec * 100, 2)

    # Get percentage of lines covered (All)
    def line_coverage(self) -> float:
        dec = 1 - len(self.unres_all_lines) / len(self.all_lines)
        return round(dec * 100, 2)

    # Get percentage of lines covered with only CMUDict
    def line_coverage_cmu(self) -> float:
        dec = len(self.all_lines_only_cmu) / len(self.all_lines)
        return round(dec * 100, 2)

    # Get percentage of lines covered with CMUDict + H2p
    def line_coverage_cmu_het(self) -> float:
        # All resolved lines
        all_res = len(self.all_lines) - len(self.unres_all_lines)
        # Remove lines containing features
        cmu_h2p_res = all_res - len(self.all_lines_cont_fet)
        dec = cmu_h2p_res / len(self.all_lines)
        return round(dec * 100, 2)

    # Get percentage of words covered (All)
    def word_coverage(self) -> float:
        dec = 1 - len(self.unres_all_words) / len(self.all_words)
        return round(dec * 100, 2)

    # Get percentage of heteronyms containing lines
    def percent_line_het(self) -> float:
        dec = len(self.all_lines_cont_het) / len(self.all_lines)
        return round(dec * 100, 2)

    # Get percentage of words resolved by H2p
    def percent_word_h2p(self) -> float:
        dec = self.n_words_het / self.n_words_res
        return round(dec * 100, 2)

    # Get percentage of words resolved by CMU
    def percent_word_cmu(self) -> float:
        dec = self.n_words_cmu / self.n_words_res
        return round(dec * 100, 2)
