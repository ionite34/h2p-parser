import re

import pytest
from h2p_parser.text import numbers


def test__remove_commas():
    text = "In 523,650,150 line."
    expected = "In 523650150 line."
    result = re.sub(numbers._comma_number_re, numbers._remove_commas, text)
    assert result == expected


def test__expand_decimal_point():
    text = "In 523.650150 line."
    expected = "In 523 point 650150 line."
    text = re.sub(numbers._decimal_number_re, numbers._expand_decimal_point, text)
    assert text == expected


@pytest.mark.parametrize("text, expected", [
    ("In $523 line.", "In five hundred and twenty-three dollars line."),
    ("In $595.99 line.", "In five hundred and ninety-five dollars, ninety-nine cents line."),
    ("In $0 line.", "In zero dollars line."),
    ("In €50 line.", "In fifty euros line."),
    ("In £50 line.", "In fifty pounds line."),
    ("In £2,000,000 line.", "In two million pounds line."),
    ("In $2,000,000,000 line.", "In two billion dollars line."),
])
def test__expand_currency(text, expected):
    result = re.sub(numbers._currency_re, numbers._expand_currency, text)
    assert result == expected


@pytest.mark.parametrize("text, expected", [
    ("1.785", "one point seven eight five"),
    ("0.800", "zero point eight zero zero"),
    ("0.00", "zero point zero zero"),
    ("0.99", "zero point nine nine"),
    ("0.9", "zero point nine"),
])
def test__expand_hundreds(text, expected):
    result = numbers._expand_hundreds(text)
    assert result == expected


@pytest.mark.parametrize("text, expected", [
    ("1st, 2nd, 3rd, 4th", "first, second, third, fourth"),
    ("57th", "fifty-seventh"),
    ("593rd", "five hundred and ninety-third"),
])
def test__expand_ordinal(text, expected):
    result = re.sub(numbers._ordinal_re, numbers._expand_ordinal, text)
    assert result == expected


@pytest.mark.parametrize("text, expected", [
    (r"23C equals 73.4F", "twenty-three celsius equals seventy-three point four fahrenheit"),
    (r"57m equals 1.5km", "fifty-seven meters equals one point five kilometers"),
    (r"1m equals 0.3ft", "one meter equals zero point three feet"),
])
def test__expand_measurement(text, expected):
    results = re.sub(numbers._measurement_re, numbers._expand_measurement, text)
    assert results == expected


def test__expand_range():
    sample = "1-3"
    expected = "1 to 3"
    result = re.sub(numbers._range_re, numbers._expand_range, sample)
    assert result == expected


@pytest.mark.parametrize("text, expected", [
    ("58x70", "58 by 70"),
    ("5x7", "5 by 7"),
])
def test__expand_multiply(text, expected):
    result = re.sub(numbers._multiply_re, numbers._expand_multiply, text)
    assert result == expected


@pytest.mark.parametrize("text, expected", [
    ("IV", "4"),
    ("XVII", "17"),
    ("XCIX", "99"),
    ("In II line.", "In 2 line."),
])
def test__expand_roman(text, expected):
    result = re.sub(numbers._roman_re, numbers._expand_roman, text)
    assert result == expected


@pytest.mark.parametrize("text, expected", [
    ("585", "five hundred and eighty five"),
    ("1200", "twelve hundred"),
    ("2000", "two thousand"),
    ("2005", "two thousand five"),
    ("2801", "twenty eight oh one"),
    ("2000's", "two thousand's"),
    ("1720's", "seventeen twenties"),
    ("5890", "five thousand eight hundred and ninety"),
    ("6500000", "six million five hundred thousand"),
    ("1000000", "one million"),
])
def test__expand_number(text, expected):
    result = re.sub(numbers._number_re, numbers._expand_number, text)
    assert result == expected


# Combined Usage
@pytest.mark.parametrize("text, expected", [
    ("In $523 line.", "In five hundred and twenty-three dollars line."),
    ("In $595.99 line.", "In five hundred and ninety-five dollars, ninety-nine cents line."),
    ("In $0 line.", "In zero dollars line."),
    ("In €50 line.", "In fifty euros line."),
    ("In £50 line.", "In fifty pounds line."),
])
def test__normalize_numbers(text, expected):
    result = numbers.normalize_numbers(text)
    assert result == expected
