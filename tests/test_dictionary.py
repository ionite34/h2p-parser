from unittest import TestCase
from unittest.mock import patch, mock_open
from h2p_parser.dictionary import Dictionary


class TestDictionary(TestCase):
    def setUp(self):
        self.file_mock_path = "file/path/mock"
        self.file_mock_content = """
        {
            "absent": {
                "VERB": "AH1 B S AE1 N T",
                "DEFAULT": "AE1 B S AH0 N T"
            },
            "abstract": {
                "VERB": "AE0 B S T R AE1 K T",
                "DEFAULT": "AE1 B S T R AE2 K T"
            }
        }
        """

    # Test initialization exceptions
    def test_dictionary_init_ex_notExist(self):
        # Try to use a file that doesn't exist
        with self.assertRaises(FileNotFoundError):
            Dictionary("/tmp/file_that_does_not_exist.txt")

    # Test default initialization
    def test_dictionary_init_default(self):
        # Test default mode
        with patch('builtins.open', mock_open(read_data=self.file_mock_content)) as mock_file:
            assert open("path/to/open").read() == self.file_mock_content
            dictionary = Dictionary()
            self.assertEqual(dictionary.dictionary,
                             {'absent': {'VERB': 'AH1 B S AE1 N T',
                                         'DEFAULT': 'AE1 B S AH0 N T'},
                              'abstract': {'VERB': 'AE0 B S T R AE1 K T',
                                           'DEFAULT': 'AE1 B S T R AE2 K T'}})
            # ock_file.assert_called_with("path/to/open")

    # Test contains method
    def test_contains(self):
        dictionary = Dictionary()
        self.assertTrue(dictionary.contains("absent"))
        self.assertTrue(dictionary.contains("ABsTRAct"))
        self.assertFalse(dictionary.contains("another"))

    # Test get_phoneme method
    def test_get_phoneme(self):
        dictionary = Dictionary()
        # Test Verb
        self.assertEqual(dictionary.get_phoneme("absent", "VBD"), "AH1 B S AE1 N T")
        self.assertEqual(dictionary.get_phoneme("abstract", "VB"), "AE0 B S T R AE1 K T")
        # Test Noun
        self.assertEqual(dictionary.get_phoneme("absent", "NNS"), "AE1 B S AH0 N T")
        self.assertEqual(dictionary.get_phoneme("abstract", "NN"), "AE1 B S T R AE2 K T")
        # Test Unknown default
        self.assertEqual(dictionary.get_phoneme("absent", "RP"), "AE1 B S AH0 N T")
        self.assertEqual(dictionary.get_phoneme("abstract", "UH"), "AE1 B S T R AE2 K T")


