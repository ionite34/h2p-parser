import random

import pytest

from h2p_parser.h2p import replace_first

# List of lines
ex_lines = [
    "The cat read the book. It was a good book to read.",
    "You should absent yourself from the meeting. Then you would be absent.",
    "The machine would automatically reject products. These were the reject products.",
]

# List of expected results
ex_expected_results = [
    "The cat {R EH1 D} the book. It was a good book to {R IY1 D}.",
    "You should {AH1 B S AE1 N T} yourself from the meeting. Then you would be {AE1 B S AH0 N T}.",
    "The machine would automatically {R IH0 JH EH1 K T} products. These were the {R IY1 JH EH0 K T} products."
]


# Function to generate test lines with n sentences, randomly chosen from the list of lines
# The number of heteronyms would be 2n
def gen_line(n):
    # List of lines
    lines = [
        "The cat read the book. It was a good book to read.",
        "You should absent yourself from the meeting. Then you would be absent.",
        "The machine would automatically reject products. These were the reject products.",
    ]
    test_line = ""
    # Loop through n sentences
    for i in range(n):
        # Add space if not the first part
        if not i == 0:
            test_line += " "
        test_line += (random.choice(lines))
    return test_line


# Test Data, for contains_het()
# List of tuples, each tuple contains:
# - Line to test
# - Expected result (True/False)
contains_het_data = [
    ("The cat read the book. It was a good book to read.", True),
    ("The effect was absent.", True),
    ("Symbols like !, ?, and ;", False),
    ("The product was a reject.", True),
    ("", False), (" ", False), ("\n", False), ("\t", False)
]


# Test the contains_het function
@pytest.mark.parametrize("line, expected", contains_het_data)
def test_contains_het(h2p, line, expected):
    assert h2p.contains_het(line) == expected


# Test the replace_het function
@pytest.mark.parametrize("line, expected", zip(ex_lines, ex_expected_results))
def test_replace_het(h2p, line, expected):
    assert h2p.replace_het(line) == expected


# Test the replace_het_list function
def test_replace_het_list(h2p):
    results = h2p.replace_het_list(ex_lines)
    for result, expected in zip(results, ex_expected_results):
        assert expected == result


replace_first_data = [
    ("the", "re", "The cat read the book.", "re cat read the book."),
    ("the", "{re mult}", "The effect was absent.", "{re mult} effect was absent."),
    ("the", "re", "Symbols !, ?, and ;", "Symbols !, ?, and ;")
]


# Test for the test_replace_first function
@pytest.mark.parametrize("search, replace, line, expected", replace_first_data)
def test_replace_first(search, replace, line, expected):
    assert replace_first(search, replace, line) == expected
