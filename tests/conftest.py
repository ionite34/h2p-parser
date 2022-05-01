# Fixtures for dictionary setup
import pytest
import pytest_mock
import unittest.mock as mock
from h2p_parser import dictionary
from h2p_parser import dict_reader
from h2p_parser.h2p import H2p


file_mock_path = "path/to/custom_dict.json"
file_mock_content = """
{
    "absent": {
        "VERB": "AH1 B S AE1 N T",
        "DEFAULT": "AE1 B S AH0 N T"
    },
    "abstract": {
        "VERB": "AE0 B S T R AE1 K T",
        "DEFAULT": "AE1 B S T R AE2 K T"
    },
    "reject": {
        "VERB": "R IH0 JH EH1 K T",
        "DEFAULT": "R IY1 JH EH0 K T"
    },
    "read": {
        "VBD": "R EH1 D",
        "VBN": "R EH1 D",
        "VBP": "R EH1 D",
        "DEFAULT": "R IY1 D"
    },
    "(No-Default)": {
        "VBD": "R EH1 D",
        "VBN": "R EH1 D",
        "VBP": "R EH1 D"
    }
}
"""
cmu_dict_path = "path/to/custom_cmu.txt"
cmu_dict_content = [
    ";;; This is a comment",
    ";;; This is another comment",
    "; This might be a comment",
    "",
    "!EXCLAMATION-POINT  EH2 K S K L AH0 M EY1 SH AH0 N P OY2 N T",
    "\"CLOSE-QUOTE  K L OW1 Z K W OW1 T",
    "#HASH-MARK  HH AE1 M AA2 R K",
    "%PERCENT  P ER0 S EH1 N T",
    "&AMPERSAND  AE1 M P ER0 S AE2 N D",
    "'COURSE  K AO1 R S",
    "(PAREN  P ER0 EH1 N",
    ")END-PAREN  EH1 N D P ER0 EH1 N",
    "PARK  P AA1 R K",
    "CONSOLE  K AA1 N S OW0 L",
    "CONSOLE  K AA1 N S OW0 L",
    "CONSOLE(1)  K AH0 N S OW1 L"
]


# noinspection PyUnusedLocal
def always_exists(path):
    return True


@pytest.fixture
# Creates a H2p instance using mock dictionary
def h2p(mocker) -> H2p:
    # Patch builtins.open
    mocked_dict_data = mock.mock_open(read_data=file_mock_content)
    with mock.patch('builtins.open', mocked_dict_data):
        # Patch Dictionary exist check
        mocker.patch.object(dictionary, 'exists', side_effect=always_exists)
        # Create H2p object
        result = H2p(file_mock_path)
    assert isinstance(result, H2p)
    assert result.dict.file_name == file_mock_path
    yield result


@pytest.fixture
# Creates a Dictionary object using mock dictionary
def mock_dict(mocker) -> dictionary.Dictionary:
    # Patch builtins.open
    mocked_dict_data = mock.mock_open(read_data=file_mock_content)
    with mock.patch('builtins.open', mocked_dict_data):
        # Patch Dictionary exist check
        mocker.patch.object(dictionary, 'exists', side_effect=always_exists)
        # Create Dictionary object
        result = dictionary.Dictionary(file_mock_path)
    assert isinstance(result, dictionary.Dictionary)
    assert result.file_name == file_mock_path
    yield result


@pytest.fixture
# Creates a Dictionary object using default path
def mock_dict_def(mocker) -> dictionary.Dictionary:
    # Patch Dictionary exist check
    mocker.patch.object(dictionary, 'exists', side_effect=always_exists)
    # Create Dictionary object
    result = dictionary.Dictionary()
    assert isinstance(result, dictionary.Dictionary)
    assert result.file_name == "dict.json"
    yield result


# Creates a dict_reader with mock dictionary
@pytest.fixture
def mock_dict_reader() -> dict_reader.DictReader:
    # Patch builtins.open
    mocked_dict_data = mock.mock_open(read_data='\n'.join(cmu_dict_content[1:]))
    with mock.patch('builtins.open', mocked_dict_data):
        result = dict_reader.DictReader(cmu_dict_path)
    assert isinstance(result, dict_reader.DictReader)
    assert result.filename == cmu_dict_path
    yield result


# Creates a dict_reader with live nltk dictionary
@pytest.fixture
def mock_dict_reader_live() -> dict_reader.DictReader:
    result = dict_reader.DictReader()
    assert isinstance(result, dict_reader.DictReader)
    yield result
