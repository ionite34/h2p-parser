import pytest
from h2p_parser.cmudictext import CMUDictExt
from h2p_parser.processors import Processor


@pytest.fixture(scope="module")
def cde():
    yield CMUDictExt()


@pytest.fixture(scope="module")
def pc(cde):
    yield Processor(cde)


# noinspection SpellCheckingInspection
@pytest.mark.parametrize("word, expected", [
    ("CLUKNM", None),
    ("Butch's", "B UH1 CH IH0 Z"),  # Case 1
    ("Rose's", "R OW1 Z IH0 Z"),
    ("Fay's", "F EY1 Z"),  # Case 2
    ("Paul's", "P AO1 L Z"),
    ("Hope's", "HH OW1 P S"),  # Case 3
    ("Ruth's", "R UW1 TH S"),
])
def test_auto_possessives(pc, word, expected):
    result = pc.auto_possessives(word)
    if result is not None:
        result = " ".join(result)
    assert result == expected


# noinspection SpellCheckingInspection
@pytest.mark.parametrize("word, expected", [
    ("UNKN'll", None),
    ("System'll", "S IH1 S T AH0 M AH0 L"),
    ("Cyprus'll", "S AY1 P R AH0 S AH0 L"),
    ("Victory'd", "V IH1 K T ER0 IY0 D"),
    ("Such'd", "S AH1 CH D"),
])
def test_auto_contractions(pc, word, expected):
    result = pc.auto_contractions(word)
    if result is not None:
        result = " ".join(result)
    assert result == expected


# noinspection SpellCheckingInspection
@pytest.mark.parametrize("word, expected", [
    ("UNKN-UNKNV", None),
    ("Get-a-toy", "G EH1 T AH0 T OY1"),
    ("G-to-P", "JH IY1 T UW1 P IY1"),
])
def test_auto_hyphenated(pc, word, expected):
    result = pc.auto_hyphenated(word)
    assert result == expected


# noinspection SpellCheckingInspection
@pytest.mark.parametrize("word, expected", [
    ("UNKNUNKNV", None),
    ("Getatoy", "G EH1 T AH0 T OY1"),
    ("JetBrains", "JH EH1 T B R EY1 N Z"),
    ("Superfreeze", "S UW1 P ER0 F R IY1 Z"),
])
def test_auto_compound(pc, word, expected):
    result = pc.auto_compound(word)
    assert result == expected


# noinspection SpellCheckingInspection
@pytest.mark.parametrize("word, expected", [
    ("UNKNs", None),
    ("Whites", "W AY1 T S"),
    ("Oranges", "AO1 R AH0 N JH IH0 Z"),
    ("MarkZeroes", "M AA1 R K Z IH1 R OW0 Z"),
    ("TrueCods", "T R UW1 K AA1 D Z"),
])
def test_auto_plural(pc, word, expected):
    result = pc.auto_plural(word)
    if result is not None:
        result = " ".join(result)
    assert result == expected


# noinspection SpellCheckingInspection
@pytest.mark.parametrize("word, expected", [
    ("unkning", None),
    ("unkningly", None),
    ("unknly", None),
    ("Codsly", "K AA1 D Z L IY0"),
    ("Divinationly", "D IH2 V AH0 N EY1 SH AH0 N L IY0"),
    ("Superfreezing", "S UW1 P ER0 F R IY1 Z IH0 NG"),
    ("SuperDivining", "S UW1 P ER0 D IH0 V AY1 N IH0 NG"),
    ("SuperSuching", "S UW1 P ER0 S AH1 CH IH0 NG"),
])
def test_auto_stem(pc, word, expected):
    result = pc.auto_stem(word)
    assert result == expected


# noinspection SpellCheckingInspection
@pytest.mark.parametrize("word, expected", [
    ("ABCUNKWN", None),
    ("SuperFreeze", "S UW1 P ER0 F R IY1 Z"),
    ("SuperDerakk", "S UW1 P ER0 D IY1 R AE1 K"),
])
def test_auto_compound_l2(pc, word, expected):
    result = pc.auto_compound_l2(word)
    assert result == expected
