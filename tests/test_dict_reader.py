import pytest
import pytest_mock
import nltk
from conftest import cmu_dict_content
from h2p_parser import dict_reader


# Test Init with Mock Data
def test_init(mock_dict_reader):
    # Test the init function of the DictReader class
    dr = mock_dict_reader
    assert isinstance(dr, dict_reader.DictReader)
    assert len(dr.dict) == (len(cmu_dict_content) - 5)
    r1 = dr.dict["park"]
    assert len(r1) == 1
    assert isinstance(r1, list)
    assert isinstance(r1[0], list)
    assert r1[0] == ["P", "AA1", "R", "K"]


# Test Init with Default (live from nltk)
def test_init_default(mock_dict_reader_live):
    # Test the init function of the DictReader class
    dr = mock_dict_reader_live
    assert isinstance(dr, dict_reader.DictReader)
    assert len(dr.dict) > 123400
    r1 = dr.dict["park"]
    assert len(r1) == 1
    assert isinstance(r1, list)
    assert isinstance(r1[0], list)
    assert r1[0] == ["P", "AA1", "R", "K"]


# Test Parse Dict
@pytest.mark.parametrize("word, phoneme, index", [
    ("#hash-mark", ['HH', 'AE1', 'M', 'AA2', 'R', 'K'], 0),
    ("park", ['P', 'AA1', 'R', 'K'], 0),
    ("console", ['K', 'AA1', 'N', 'S', 'OW0', 'L'], 0),
    ("console", ['K', 'AH0', 'N', 'S', 'OW1', 'L'], 1),
    ("console(1)", ['K', 'AH0', 'N', 'S', 'OW1', 'L'], 0),
])
def test_parse_dict(mock_dict_reader, word, phoneme, index):
    dr = mock_dict_reader
    assert dr.dict[word][index] == phoneme


# Fake Download Function
# noinspection PyUnusedLocal
def fake_download(file):
    return


# Test nltk download
def test_get_cmu_dict(mocker, mock_dict_reader_live):
    # We need to patch nltk.data.find to raise an error
    mocker.patch("nltk.data.find", side_effect=LookupError)
    mocker.patch("dict_reader.cmudict.dict", return_value={})
    downloader = mocker.patch("nltk.download", side_effect=fake_download)
    var = dict_reader.get_cmu_dict()
    assert isinstance(var, dict)
    downloader.assert_called_once_with("cmudict")
