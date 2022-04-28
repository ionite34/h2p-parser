from unittest import TestCase
from unittest.mock import patch, mock_open
from h2p_parser.dictionary import Dictionary


# Replacer for file exists check
# noinspection PyUnusedLocal
def always_exists(path):
    return True


# Replaces importlib.resources.path
# noinspection PyUnusedLocal
def always_none(a, b):
    return None


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
            },
            "read": {
                "VBD": "R EH1 D",
                "VBN": "R EH1 D",
                "VBP": "R EH1 D",
                "DEFAULT": "R IY1 D"
            }
        }
        """
        self.expected_dict = {'absent': {'VERB': 'AH1 B S AE1 N T',
                                         'DEFAULT': 'AE1 B S AH0 N T'},
                              'abstract': {'VERB': 'AE0 B S T R AE1 K T',
                                           'DEFAULT': 'AE1 B S T R AE2 K T'},
                              'read': {'VBD': 'R EH1 D',
                                       'VBN': 'R EH1 D',
                                       'VBP': 'R EH1 D',
                                       'DEFAULT': 'R IY1 D'},
                              }

    # Constructs a dictionary while skipping file existence check
    # noinspection PyUnusedLocal
    @patch('h2p_parser.dictionary.exists', side_effect=always_exists)
    def get_dict(self, exists_function, path=None):
        with patch('builtins.open', mock_open(read_data=self.file_mock_content)):
            assert open("path/to/open").read() == self.file_mock_content
            return Dictionary(path)

    # Test Initialization
    def test_init(self):
        test_dict = self.get_dict()
        self.assertEqual(test_dict.dictionary, self.expected_dict)
        self.assertEqual(test_dict.file_name, "dict.json")
        self.assertEqual(test_dict.use_default, True)

    # Test Loading
    def test_load_dictionary(self):
        self.test_dictionary_init_default_ex()
        self.test_dictionary_init_custom_ex()
        self.test_dictionary_init_default()
        self.test_dictionary_init_custom()

    # Test initialization exceptions - Default Dictionary
    @patch('h2p_parser.dictionary.importlib.resources.path', side_effect=always_none)
    def test_dictionary_init_default_ex(self, mock_importlib):
        # Try to use a file that doesn't exist
        # Assert exception is raised
        with self.assertRaises(FileNotFoundError) as context:
            Dictionary()
        # Check if the exception message is correct
        self.assertEqual("Data folder not found",
                         str(context.exception))

    # Test initialization exceptions - Custom Dictionary
    def test_dictionary_init_custom_ex(self):
        # Try to use a file that doesn't exist
        # Assert exception is raised
        with self.assertRaises(FileNotFoundError) as context:
            Dictionary("file_not_exist.json")
        # Check if the exception message is correct
        self.assertEqual("Dictionary file_not_exist.json file not found",
                         str(context.exception))

    # Test default initialization
    def test_dictionary_init_default(self):
        # Create dictionary with default path and mock content
        test_dict = self.get_dict()
        # Check if it's the same as the expected dictionary
        self.assertEqual(self.expected_dict, test_dict.dictionary)

    # Test initialization with a file
    def test_dictionary_init_custom(self):
        # Create dictionary with a file path and mock content
        test_dict = self.get_dict(self.file_mock_path)
        # Check if it's the same as the expected dictionary
        self.assertEqual(self.expected_dict, test_dict.dictionary)

    # Test contains method
    def test_contains(self):
        test_dict = self.get_dict()
        self.assertTrue(test_dict.contains("absent"))
        self.assertTrue(test_dict.contains("ABsTRAct"))
        self.assertFalse(test_dict.contains("another"))

    # Test get_phoneme method
    def test_get_phoneme(self):
        test_dict = self.get_dict()
        # Test Verb
        self.assertEqual(test_dict.get_phoneme("absent", "VBD"), "AH1 B S AE1 N T")
        self.assertEqual(test_dict.get_phoneme("abstract", "VB"), "AE0 B S T R AE1 K T")
        # Test Noun
        self.assertEqual(test_dict.get_phoneme("absent", "NNS"), "AE1 B S AH0 N T")
        self.assertEqual(test_dict.get_phoneme("abstract", "NN"), "AE1 B S T R AE2 K T")
        # Test Unknown default
        self.assertEqual(test_dict.get_phoneme("absent", "RP"), "AE1 B S AH0 N T")
        self.assertEqual(test_dict.get_phoneme("abstract", "UH"), "AE1 B S T R AE2 K T")
        # Test Specific
        self.assertEqual(test_dict.get_phoneme("read", "VBD"), "R EH1 D")
        self.assertEqual(test_dict.get_phoneme("read", "VBN"), "R EH1 D")
        self.assertEqual(test_dict.get_phoneme("read", "VBP"), "R EH1 D")
        self.assertEqual(test_dict.get_phoneme("read", "NN"), "R IY1 D")
