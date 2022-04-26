from unittest import TestCase
import filter


# noinspection SpellCheckingInspection
class Test(TestCase):
    # Test for accents
    def test_filter_text_accents(self):
        orig = "áéíóú"
        expect = "aeiou"
        result = filter.filter_text(orig)
        self.assertEqual(expect, result)

    # Test for lowercase
    def test_filter_text_lowercase(self):
        orig = "TESTcase"
        expect = "testcase"
        result = filter.filter_text(orig)
        self.assertEqual(expect, result)

    # Test for puncutations removal
    def test_filter_text_punctuation(self):
        # Test safe punctuation
        orig = "w, case[s]?! 'Ts"
        expect = "w, cases?! 'ts"
        result = filter.filter_text(orig)
        self.assertEqual(expect, result)

        # Test invalid punctuation
        orig = r"te@#$%^&*()_+=[]{};:\"\/<>`~st"
        expect = "test"
        result = filter.filter_text(orig)
        self.assertEqual(expect, result)

