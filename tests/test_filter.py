from unittest import TestCase
import h2p_parser.filter as h2p_filter


# noinspection SpellCheckingInspection
class Test(TestCase):
    # Test for accents
    def test_filter_text_accents(self):
        orig = "áéíóú"
        expect = "aeiou"
        result = h2p_filter.filter_text(orig)
        self.assertEqual(expect, result)

    # Test for lowercase
    def test_filter_text_lowercase(self):
        orig = "TESTcase"
        expect = "testcase"
        result = h2p_filter.filter_text(orig)
        self.assertEqual(expect, result)

    # Test for puncutations removal
    def test_filter_text_punctuation(self):
        # Test safe punctuation
        orig = "w, case[s]?! 'Ts"
        expect = "w, cases?! 'ts"
        result = h2p_filter.filter_text(orig)
        self.assertEqual(expect, result)

        # Test invalid punctuation
        orig = r"te@#$%^&*()_+=[]{};:\"\/<>`~st"
        expect = "test"
        result = h2p_filter.filter_text(orig)
        self.assertEqual(expect, result)

    # Test for multiple spaces removal
    def test_filter_text_spaces(self):
        orig = "In some  line   like    this."
        expect = "in some line like this."
        result = h2p_filter.filter_text(orig)
        self.assertEqual(expect, result)

    # Test for numbers mode
    def test_filter_text_numbers(self):
        orig = "In 123 line."
        expected1 = "in 123 line."
        expected2 = "in line."
        # Mode True
        with self.subTest("Allow numbers mode"):
            result = h2p_filter.filter_text(orig, True)
            self.assertEqual(expected1, result)
        with self.subTest("Disallow numbers mode"):
            result = h2p_filter.filter_text(orig, False)
            self.assertEqual(expected2, result)

