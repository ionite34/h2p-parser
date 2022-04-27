from unittest import TestCase
from unittest.mock import patch
import dict_reader
from h2p_parser.dict_reader import DictReader
import h2p_parser.dict_reader


# Mock for read_dict
# noinspection PyUnusedLocal
def read_dict(filename):
    test_line_list = [
        ";;; This is a comment",
        ";;; This is another comment",
        "; This might be a comment",
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
        "CONSOLE(1)  K AH0 N S OW1 L"
    ]
    return test_line_list


class TestDictReader(TestCase):
    def setUp(self):
        # Define test line list
        self.test_line_list = [
            ";;; This is a comment",
            ";;; This is another comment",
            "; This might be a comment",
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
            "CONSOLE(1)  K AH0 N S OW1 L"
        ]

    # Test Init
    # Mock the read_dict function
    @patch('h2p_parser.dict_reader.read_dict', side_effect=read_dict)
    def test_init(self, mock_read_dict):
        # Create object
        target = DictReader("test_dict.txt")
        self.assertIsInstance(target, DictReader)

    def test_parse_dict(self):
        # Test using test line list
        result = dict_reader.parse_dict(self.test_line_list)
        # Verify result length correct
        self.assertEqual(len(result), len(self.test_line_list)-3)
        # Verify result contains expected values
        self.assertEqual(result["#HASH-MARK"][0], "HH AE1 M AA2 R K")
        self.assertEqual(result["PARK"][0], "P AA1 R K")
        # Test multi-entries
        self.assertEqual(result["CONSOLE"][0], "K AA1 N S OW0 L")
        self.assertEqual(result["CONSOLE"][1], "K AH0 N S OW1 L")
