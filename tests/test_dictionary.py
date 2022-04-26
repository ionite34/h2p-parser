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

    def test_read(self):
        pass
