# Tool to test the performance of various operations.
import random
from statistics import mean
from unittest.mock import patch, mock_open

from h2p_parser.h2p import H2p
from timeit import default_timer as timer


# Method to convert time to milliseconds rounded to 3 decimal places, as string
def to_ms(time_sec):
    return str(round(time_sec * 1000, 3))


# Method to convert 2 int values to string percentage delta rounded to 3 decimal places, as string
def to_percent(value1, value2):
    if (value1 == 0) or (value2 == 0):
        return "0.000"
    if value1 < value2:
        return str(round(((value2 - value1) / value2) * 100, 3))
    elif value1 > value2:
        return str(round(((value1 - value2) / value1) * 100, 3))
    return "0.000"


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


# noinspection PyUnusedLocal
def always_exists(path):
    return True


class Perf:
    def __init__(self):
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
        self.h2p = self.get_h2p()

    # noinspection PyUnusedLocal
    @patch('h2p_parser.dictionary.exists', side_effect=always_exists)
    def get_h2p(self, exists_function):
        with patch('builtins.open', mock_open(read_data=self.file_mock_content)):
            result = H2p("path/to/open")
        result.preload()
        return result

    # Measuring the performance of the replace_het function
    def test_performance_replace_het(self, n):
        # Method to test single line performance
        def perf_test(line_in, startup=False):
            # Start startup time measurement
            start = timer()
            # Call setUp function, if startup is True
            if startup:
                self.h2p = self.get_h2p()
            # Get one result
            self.h2p.replace_het(line_in)
            # Stop time measurement
            end = timer()
            # Calculate the time and return it
            return end - start

        # Generate a test line
        t1 = gen_line(2)

        # Loop n times, get 1 startup and 2 subsequent results, append to lists
        startup_times = []
        sub1_times = []
        sub2_times = []
        for i in range(n):
            startup_times.append(perf_test(t1, startup=True))
            sub1_times.append(perf_test(t1))
            sub2_times.append(perf_test(t1))

        # Calculate the average times
        startup_avg = mean(startup_times)
        sub1_avg = mean(sub1_times)
        sub2_avg = mean(sub2_times)

        # Report both as ms, round to 3 decimal places
        print("-" * 10)
        print("Perf Test: Replace Het")
        print(f"Avg Startup time: {to_ms(startup_avg)} ms")
        print(f'First 5 Startup times: {[to_ms(t) for t in startup_times[:5]]} ms')
        print(f"Avg 2nd Subsequent time: {to_ms(sub1_avg)} ms")
        print(f"Avg 3rd Subsequent time: {to_ms(sub2_avg)} ms")

    # Measuring performance of replace_het vs replace_het_list
    def test_performance_replace_het_list(self, n):
        # Single Line Method
        def perf_test(line_in):
            start = timer()
            self.h2p.replace_het(line_in)
            end = timer()
            return end - start

        # List Method
        def perf_test_list(list_in):
            start = timer()
            self.h2p.replace_het_list(list_in)
            end = timer()
            return end - start

        # Generate a list of lines by random selection using gen_line
        gen_lines = []
        for i in range(n):
            gen_lines.append(gen_line(1))

        def run_test(lines):
            # Run using list call
            list_total_time = perf_test_list(lines)
            # Run using single calls
            single_times = []
            for line in lines:
                single_times.append(perf_test(line))
            # Calculate sum of single times
            single_time_sum = sum(single_times)
            return single_time_sum, list_total_time

        # Call run_test 5 times, use the average of the best 3 results
        all_runs_single = []
        all_runs_list = []
        for i in range(5):
            single_time, list_time = run_test(gen_lines)
            all_runs_single.append(single_time)
            all_runs_list.append(list_time)
        single_avg = mean(sorted(all_runs_single)[:3])
        list_avg = mean(sorted(all_runs_list)[:3])

        # Report both as ms, round to 3 decimal places
        print("-" * 10)
        print(f"Perf Test: Replace Het List - Size {n}")
        print(f"[replace_het] x {n} -> Time: {to_ms(single_avg)} ms")
        print(f"[replace_het_list] -> Time: {to_ms(list_avg)} ms")
        # Determine if the list method is faster in print
        if single_avg > list_avg:
            print("[replace_het_list] is faster")
        else:
            print("[replace_het] is faster")
        print(f"Difference: {to_ms(single_avg - list_avg)} ms, {to_percent(single_avg, list_avg)}%")


if __name__ == '__main__':
    p = Perf()
    # Perf Test for replace_het
    p.test_performance_replace_het(30)
    # Perf Test for replace_het_list vs replace_het
    p.test_performance_replace_het_list(1)
    p.test_performance_replace_het_list(2)
    p.test_performance_replace_het_list(10)
    p.test_performance_replace_het_list(32)
    p.test_performance_replace_het_list(64)
    p.test_performance_replace_het_list(128)
    p.test_performance_replace_het_list(256)
