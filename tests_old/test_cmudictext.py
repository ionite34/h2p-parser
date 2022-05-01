from unittest import TestCase

from h2p_parser.h2p import H2p
from h2p_parser.cmudictext import CMUDictExt


class TestCMUDictExt(TestCase):
    def setUp(self):
        # List of test lines
        self.ex_lines = [
            "The cat read the book. It was a good book to read.",
            "You should absent yourself from the meeting. Then you would be absent.",
            "The machine would automatically reject products. These were the reject products.",
        ]

        # List of expected results
        self.ex_expected_results = [
            "{DH AH0} {K AE1 T} {R EH1 D} {DH AH0} {B UH1 K}. {IH1 T} {W AA1 Z} {AH0} "
            "{G UH1 D} {B UH1 K} {T UW1} {R IY1 D}.",
            "{Y UW1} {SH UH1 D} {AH1 B S AE1 N T} {Y ER0 S EH1 L F} {F R AH1 M} {DH AH0} {M IY1 T IH0 NG}. "
            "{DH EH1 N} {Y UW1} {W UH1 D} {B IY1} {AE1 B S AH0 N T}.",
            "{DH AH0} {M AH0 SH IY1 N} {W UH1 D} {AO2 T AH0 M AE1 T IH0 K L IY0} {R IH0 JH EH1 K T} "
            "{P R AA1 D AH0 K T S}. {DH IY1 Z} {W ER0} {DH AH0} {R IY1 JH EH0 K T} {P R AA1 D AH0 K T S}."
        ]
        self.target = CMUDictExt()
        self.assertIsInstance(self.target, CMUDictExt)

    def test_cmudict_ext(self):
        # Test all default initialization
        self.assertIsInstance(self.target.dict, dict)
        self.assertIsInstance(self.target.h2p, H2p)
        # Test value error for unresolved_mode
        with self.assertRaises(ValueError):
            CMUDictExt(unresolved_mode='invalid')

    def test_lookup(self):
        self.assertEqual(' '.join(self.target.lookup("cat")[0]), "K AE1 T")
        self.assertEqual(' '.join(self.target.lookup("CaT")[0]), "K AE1 T")
        self.assertEqual(' '.join(self.target.lookup("CAT")[0]), "K AE1 T")
        self.assertEqual(self.target.lookup("Does_Not_Exist"), None)

    def test_convert(self):
        for i, line in enumerate(self.ex_lines):
            result = self.target.convert(line)
            expected = self.ex_expected_results[i]
            self.assertEqual(result, expected)

    # Test unknown word handling
    # Default should be 'keep'
    def test_convert_unresolved_keep(self):
        self.assertEqual(self.target.convert("DoesNotExist"), "DoesNotExist")
        self.assertEqual(self.target.convert("DoesNotExist: Such;"), "DoesNotExist: {S AH1 CH};")
        self.assertEqual(self.target.convert("In DoesNotExist line."), "{IH0 N} DoesNotExist {L AY1 N}.")
        # Test numbers
        self.target.process_numbers = True
        self.assertEqual(self.target.convert("1"), "{W AH1 N}")
        self.assertEqual(self.target.convert("In 1 line."), "{IH0 N} {W AH1 N} {L AY1 N}.")
        # Test numbers with process_numbers=False
        self.target.process_numbers = False
        self.assertEqual(self.target.convert("1"), "1")
        self.assertEqual(self.target.convert("In 1 line."), "{IH0 N} 1 {L AY1 N}.")

    def test_convert_unresolved_remove(self):
        self.target.unresolved_mode = 'remove'
        self.assertEqual(self.target.convert("DoesNotExist"), "")
        self.assertEqual(self.target.convert("DoesNotExist: Such;"), ": {S AH1 CH};")
        self.assertEqual(self.target.convert("In DoesNotExist line."), "{IH0 N}  {L AY1 N}.")
        # Test numbers
        self.target.process_numbers = True
        self.assertEqual(self.target.convert("1"), "{W AH1 N}")
        self.assertEqual(self.target.convert("In 1 line."), "{IH0 N} {W AH1 N} {L AY1 N}.")
        # Test numbers with process_numbers=False
        self.target.process_numbers = False
        self.assertEqual(self.target.convert("1"), "1")
        self.assertEqual(self.target.convert("In 1 line."), "{IH0 N} 1 {L AY1 N}.")

    def test_convert_unresolved_drop(self):
        self.target.unresolved_mode = 'drop'
        self.assertEqual(self.target.convert("DoesNotExist"), None)
        self.assertEqual(self.target.convert("DoesNotExist: Such;"), None)
        self.assertEqual(self.target.convert("In DoesNotExist line."), None)

    def test_convert_invalid_args(self):
        self.target.unresolved_mode = "invalid"
        with self.assertRaises(ValueError):
            self.target.convert("Does_Not_Exist")
