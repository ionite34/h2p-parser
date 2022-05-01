import pytest
from unittest import mock
from h2p_parser.utils import converter

test_data = """
# This is a comment
# More Comments
REPLAY|R IY0 P L EY1|R IY1 P L EY0|V
REPLAYS|R IY0 P L EY1 Z|R IY1 P L EY0 Z|V
REPRINT|R IY0 P R IH1 N T|R IY1 P R IH0 N T|V
REPRINTS|R IY0 P R IH1 N T S|R IY1 P R IH0 N T S|V
RERUN|R IY2 R AH1 N|R IY1 R AH0 N|VBN
RERUNS|R IY2 R AH1 N Z|R IY1 R AH0 N Z|V
RESUME|R IY0 Z UW1 M|R EH1 Z AH0 M EY2|V
RETAKE|R IY0 T EY1 K|R IY1 T EY0 K|V
"""


def test_from_binary_delim():
    # Patch the built-in open function
    mock_data = mock.mock_open(read_data=test_data)
    with mock.patch('builtins.open', mock_data):
        result = converter.from_binary_delim("path/to/file", '|')
    sub_dict = result["REPLAY"]
    assert isinstance(sub_dict, dict)
    assert len(sub_dict) == 2
    assert sub_dict["DEFAULT"] == "R IY1 P L EY0"
    assert sub_dict["VERB"] == "R IY0 P L EY1"


@pytest.mark.parametrize("data, error, msg", [
    ("REPLAY|R IY0 P L EY1|R IY1 P L EY0|V|V2", ValueError,
     "Invalid number of tokens in line: REPLAY|R IY0 P L EY1|R IY1 P L EY0|V|V2"),
    ("REP LAY|R IY0 P L EY1|R IY1 P L EY0|V", ValueError,
     "Invalid word in line: REP LAY|R IY0 P L EY1|R IY1 P L EY0|V"),
    ("REPLAY|R # P L EY1|R IY1 P L EY0|V", ValueError,
     "Invalid phonemes in line: REPLAY|R # P L EY1|R IY1 P L EY0|V"),
    ("REPLAY|R IY0 P L EY1|R IY1 P L EY0|V2", ValueError,
     "Invalid case in line: REPLAY|R IY0 P L EY1|R IY1 P L EY0|V2"),
])
def test_from_binary_delim_invalid(data, error, msg):
    # Patch the built-in open function
    mock_data = mock.mock_open(read_data=data)
    with mock.patch('builtins.open', mock_data):
        with pytest.raises(error, match=msg):
            converter.from_binary_delim("path/to/file", '|')
