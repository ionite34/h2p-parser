from unittest import TestCase
from unittest.mock import patch
from h2p_parser.dict_reader import DictReader
from h2p_parser import dict_reader
import h2p_parser.format_ph as ph


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


# Mock for nltk download error
# noinspection PyUnusedLocal
def always_error(path):
    raise LookupError("Mock error")


# Mock for nltk download success
# noinspection PyUnusedLocal
def fake_download(path):
    a = 1 + 1


# Mock for cmudict
# noinspection PyUnusedLocal
def fake_cmudict():
    return {}


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
        with self.subTest("File Mode"):
            target = DictReader("test_dict.txt")
            self.assertIsInstance(target, DictReader)
            self.assertIsInstance(target.dict, dict)
            self.assertEqual(len(target.dict), len(self.test_line_list) - 3)
            result = target.dict["park"]
            self.assertIsInstance(result, list)
            self.assertIsInstance(result[0], list)
            self.assertEqual(4, len(result[0]))
            phonemes = result[0]
            self.assertEqual(phonemes[0], "P")
            self.assertEqual(phonemes[1], "AA1")
            self.assertEqual(phonemes[2], "R")
            self.assertEqual(phonemes[3], "K")

        with self.subTest("Default mode"):
            target = DictReader()
            self.assertIsInstance(target, DictReader)
            self.assertIsInstance(target.dict, dict)
            result = target.dict["park"]
            self.assertIsInstance(result, list)
            self.assertIsInstance(result[0], list)
            self.assertEqual(4, len(result[0]))
            phonemes = result[0]
            self.assertEqual(phonemes[0], "P")
            self.assertEqual(phonemes[1], "AA1")
            self.assertEqual(phonemes[2], "R")
            self.assertEqual(phonemes[3], "K")

    def test_parse_dict(self):
        # Test using test line list
        result = dict_reader.parse_dict(self.test_line_list)
        # Verify result length correct
        self.assertEqual(len(result), len(self.test_line_list) - 3)
        # Verify result contains expected values
        self.assertEqual(result["#hash-mark"][0], ph.to_list("HH AE1 M AA2 R K"))
        self.assertEqual(result["park"][0], ph.to_list("P AA1 R K"))
        # Test multi-entries
        self.assertEqual(result["console"][0], ph.to_list("K AA1 N S OW0 L"))
        self.assertEqual(result["console"][1], ph.to_list("K AH0 N S OW1 L"))

    # @patch('h2p_parser.dict_reader.nltk.data.find', side_effect=always_error)
    # @patch('h2p_parser.dict_reader.nltk.download', side_effect=fake_download)
    def test_get_cmu_dict(self):
        # Test download (not exist mode)
        with patch('h2p_parser.dict_reader.nltk.data.find', side_effect=always_error) as patch_data:
            result = dict_reader.get_cmu_dict()
            self.assertIsInstance(result, dict)
            self.assertEqual(patch_data.call_count, 1)
