# Static Performance Tests

# noinspection SpellCheckingInspection
import random

import unicodedata
from timeit import timeit


# Function to run a method using timeit n times and returns time metrics
def run_time(method, n):
    # Run the method n times
    times = timeit(method, number=n)
    # Return the mean time
    times = times * 1000
    if times < 1:
        return times, f'{round(times * 1000, 2)} μs'
    else:
        return times, f"{round(times, 2)} ms"


# noinspection SpellCheckingInspection
def perf_accent_norm(iters):
    # Tests performance of accent normalization
    no_accents = "aeinou"
    accents = "áéíñóú"
    run_mult = [10, 100, 1000]

    # Standard mode
    def m1(text_in):
        return ''.join(char for char in unicodedata.normalize('NFD', text_in)
                       if unicodedata.category(char) != 'Mn')

    # With contains check
    def m2(text_in):
        return unicodedata.normalize('NFD', text_in)

    # loop for number of runs in run_mult
    for mult in run_mult:
        # build the lines
        no_accents_line = ''.join(random.choice(no_accents) for _ in range(mult))
        accents_line = ''.join(random.choice(accents) for _ in range(mult))

        print("-" * 10)
        print(f"Run for {mult}")
        print("-" * 5)
        print("Accents:")
        # Time m1
        t1_acc = run_time(lambda: m1(accents_line), iters)
        t2_acc = run_time(lambda: m2(accents_line), iters)
        print(f"T1, Accents: {t1_acc[1]} ms")
        print(f"T2, Accents: {t2_acc[1]} ms")
        # Calculate winner
        if t1_acc[0] < t2_acc[0]:
            # percent difference
            print(f"Type 1 is {round(t2_acc[0] / t1_acc[0] * 100, 2)}% faster")
        else:
            print(f"Type 2 is {round(t1_acc[0] / t2_acc[0] * 100, 2)}% faster")
        print("-" * 5)
        print("No Accents:")
        t1_no_acc = run_time(lambda: m1(no_accents_line), iters)
        t2_no_acc = run_time(lambda: m2(no_accents_line), iters)
        print(f"T1, No Accents: {t1_no_acc[1]}")
        print(f"T2, No Accents: {t2_no_acc[1]}")
        # Calculate winner
        if t1_no_acc[0] < t2_no_acc[0]:
            # percent difference
            print(f"Type 1 is {round(t2_no_acc[0] / t1_no_acc[0] * 100, 2)}% faster")
        else:
            print(f"Type 2 is {round(t1_no_acc[0] / t2_no_acc[0] * 100, 2)}% faster")


if __name__ == '__main__':
    perf_accent_norm(30)
