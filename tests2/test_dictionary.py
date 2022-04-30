import json

import pytest
import pytest_mock
import unittest.mock as mock

from h2p_parser.dictionary import Dictionary
import h2p_parser.dictionary as dictionary


# Test initialization of dictionary from confTest
def test_init(mock_dict):
    assert isinstance(mock_dict.dictionary, dict)
    assert mock_dict.use_default is False


# Test default initialization of dictionary
def test_init_default(mock_dict_def):
    assert isinstance(mock_dict_def.dictionary, dict)
    assert mock_dict_def.use_default is True


# Test initialization exceptions, custom file
def test_init_exceptions_custom(mock_dict):
    with pytest.raises(FileNotFoundError):
        Dictionary("file_not_exist.json")


# Test init exceptions, custom file (empty)
def test_init_exceptions_custom_empty(mocker):
    # Patch builtins.open
    mocked_dict_data = mock.mock_open(read_data="")
    with mock.patch('builtins.open', mocked_dict_data):
        # Patch Dictionary exist check
        mocker.patch.object(dictionary, 'exists', return_value=True)
        # Attempt to create Dictionary object
        msg = 'Dictionary path.json file is not valid JSON'
        with pytest.raises(ValueError, match=msg):
            with pytest.raises(json.decoder.JSONDecodeError):
                dictionary.Dictionary("path.json")


# Test initialization exceptions, default file
def test_init_exceptions_default(mocker, mock_dict_def):
    mocker.patch('h2p_parser.dictionary.pkg_resources.files', return_value=None)
    with pytest.raises(FileNotFoundError):
        Dictionary()


# Test contains
@pytest.mark.parametrize("data, exp", [
    ("absent", True),
    ("ABsTRAct", True),
    ("reject", True),
    ("another", False),
    ("##$$;;", False)
])
def test_contains(data, exp, mock_dict):
    assert mock_dict.contains(data) is exp


# Test get_phoneme
@pytest.mark.parametrize("word, pos, phoneme", [
    ("absent", "VBD", "AH1 B S AE1 N T"),
    ("abstract", "VB", "AE0 B S T R AE1 K T"),
    ("absent", "NNS", "AE1 B S AH0 N T"),
    ("abstract", "NN", "AE1 B S T R AE2 K T"),
    ("absent", "RP", "AE1 B S AH0 N T"),
    ("abstract", "UH", "AE1 B S T R AE2 K T"),
    ("read", "VBD", "R EH1 D"),
    ("read", "VBN", "R EH1 D"),
    ("read", "VBP", "R EH1 D"),
    ("read", "NN", "R IY1 D"),
    ("read", "UH", "R IY1 D"),
    ("(No-Default)", "UH", None)
])
def test_get_phoneme(word, pos, phoneme, mock_dict):
    assert mock_dict.get_phoneme(word, pos) == phoneme
