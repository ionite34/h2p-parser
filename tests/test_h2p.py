from unittest import TestCase
from unittest.mock import patch, mock_open
from h2p import H2p


# noinspection PyUnusedLocal
def always_exists(path):
    return True


class TestH2p(TestCase):

    @patch('dictionary.exists', side_effect=always_exists)
    def setUp(self, exists_function):
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
        with patch('builtins.open', mock_open(read_data=self.file_mock_content)) as mock_file:
            assert open("path/to/open").read() == self.file_mock_content
            # Override the os.path.exists function
            with patch('os.path.exists', return_value=True):
                self.h2p = H2p("path/to/open")

    def test_contains_het(self):
        # List of lines
        lines = [
            "The cat read the book.",
            "The effect was absent.",
            "Symbols like !, ?, and ;",
            "It was an abstract idea.",
            "0123456789",
            "",
            " ",
            "/n"
        ]

        # List of expected results
        expected_results = [True, True, False, True, False, False, False, False]

        # Loop through lines
        for line, expected_result in zip(lines, expected_results):
            self.assertEqual(self.h2p.contains_het(line), expected_result)

