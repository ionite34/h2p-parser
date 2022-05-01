import pytest
import h2p_parser.filter as h2p_filter


# Test for accents
# noinspection SpellCheckingInspection
@pytest.mark.parametrize("source, expected", [
    ("áéíóú", "aeiou"),
    ("ÁÉÍÓÚ", "aeiou"),
    ("àèìòù", "aeiou"),
    ("ÀÈÌÒÙ", "aeiou"),
])
def test_filter_text_accents(source, expected):
    result = h2p_filter.filter_text(source)
    assert result == expected


# Test for case
@pytest.mark.parametrize("source, expected", [
    ("TESTCase", "testcase"),
    ("TestCase", "testcase"),
    ("testcase", "testcase")
])
def test_filter_text_lowercase(source, expected):
    result = h2p_filter.filter_text(source)
    assert result == expected


# Test for invalid punctuation removal
@pytest.mark.parametrize("source, expected", [
    ("w, case[s]?! 'Ts", "w, cases?! 'ts"),
    (r"te@#$%^&*_+=[]{};:\"\/<>`~st", "test")
])
def test_filter_text_punctuation(source, expected):
    result = h2p_filter.filter_text(source)
    assert result == expected


# Test for multiple spaces removal
@pytest.mark.parametrize("source, expected", [
    ("In some  line   like    this.",
     "in some line like this."),
    ("normal spaces.",
     "normal spaces.")
])
def test_filter_text_spaces(source, expected):
    result = h2p_filter.filter_text(source)
    assert result == expected


# Test for numbers mode
@pytest.mark.parametrize("source, expected, mode_on", [
    ("1234567890", "1234567890", True),
    ("1234567890", "", False),
    ("In 1234567890 line 56.", "in line .", False)
])
def test_filter_text_numbers(source, expected, mode_on):
    result = h2p_filter.filter_text(source, mode_on)
    assert result == expected
