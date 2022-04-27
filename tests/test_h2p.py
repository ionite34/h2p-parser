import random
import time
from statistics import mean
from unittest import TestCase
from unittest.mock import patch, mock_open
from h2p import H2p
from timeit import default_timer as timer


# noinspection PyUnusedLocal
def always_exists(path):
    return True


# Function to generate test lines with n sentences, randomly chosen from the list of lines
# The number of heteronyms would be 2n
def gen_line(n):
    # List of lines
    lines = [
        "The cat read the book. It was a good book to read.",
        "You should absent yourself from the meeting. Then you would be absent.",
        "The machine would automatically reject products. These were the reject products.",
    ]
    test_line = ""
    # Loop through n sentences
    for i in range(n):
        # Add space if not the first part
        if not i == 0:
            test_line += " "
        test_line += (random.choice(lines))
    return test_line


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
            "reject": {
                "VERB": "R IH0 JH EH1 K T",
                "DEFAULT": "R IY1 JH EH0 K T"
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

    # Test the contains_het function
    def test_contains_het(self):
        # List of lines
        lines = [
            "The cat read the book.",
            "The effect was absent.",
            "Symbols like !, ?, and ;",
            "The product was a reject.",
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

    # Test the replace_het function
    def test_replace_het(self):
        # List of lines
        lines = [
            "The cat read the book. It was a good book to read.",
            "You should absent yourself from the meeting. Then you would be absent.",
            "The machine would automatically reject products. These were the reject products.",
        ]

        # List of expected results
        expected_results = [
            "The cat {R EH1 D} the book. It was a good book to {R IY1 D}.",
            "You should {AH1 B S AE1 N T} yourself from the meeting. Then you would be {AE1 B S AH0 N T}.",
            "The machine would automatically {R IH0 JH EH1 K T} products. These were the {R IY1 JH EH0 K T} products."
        ]

        # Loop through lines
        for line, expected_result in zip(lines, expected_results):
            self.assertEqual(self.h2p.replace_het(line), expected_result)

    # Measuring the performance of the replace_het function
    def test_performance_replace_het(self):
        # Method to test single line performance
        def perf_test(line_in, startup=False):
            # Start startup time measurement
            start = timer()
            # Call setUp function, if startup is True
            if startup:
                self.setUp()
            # Get one result
            self.h2p.replace_het(line_in)
            # Stop time measurement
            end = timer()
            # Calculate the time and return it
            return end - start

        # Method to convert time to milliseconds rounded to 3 decimal places, as string
        def to_ms(time_sec):
            return str(round(time_sec * 1000, 3))

        # Generate a test line
        t1 = gen_line(2)

        # Loop 30 times, get 1 startup and 2 subsequent results, append to lists
        startup_times = []
        sub1_times = []
        sub2_times = []
        for i in range(30):
            startup_times.append(perf_test(t1, startup=True))
            sub1_times.append(perf_test(t1))
            sub2_times.append(perf_test(t1))

        # Calculate the average times
        startup_avg = mean(startup_times)
        sub1_avg = mean(sub1_times)
        sub2_avg = mean(sub2_times)

        # Report both as ms, round to 3 decimal places
        print(f"Avg Startup time: {to_ms(startup_avg)} ms")
        print(f'First 5 Startup times: {[to_ms(t) for t in startup_times[:5]]} ms')
        print(f"Avg 2nd Subsequent time: {to_ms(sub1_avg)} ms")
        print(f"Avg 3rd Subsequent time: {to_ms(sub2_avg)} ms")
