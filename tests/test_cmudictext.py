from unittest import TestCase
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

    def test_cmudict_ext(self):
        # Test all default initialization
        target = CMUDictExt()
        self.assertIsInstance(target, CMUDictExt)

    def test_lookup(self):
        target = CMUDictExt()
        self.assertEqual(' '.join(target.lookup("cat")[0]), "K AE1 T")
        self.assertEqual(' '.join(target.lookup("CaT")[0]), "K AE1 T")
        self.assertEqual(' '.join(target.lookup("CAT")[0]), "K AE1 T")
        self.assertEqual(target.lookup("Does_Not_Exist"), None)

    def test_convert(self):
        # Test conversion
        target = CMUDictExt()
        for i, line in enumerate(self.ex_lines):
            result = target.convert(line)
            expected = self.ex_expected_results[i]
            self.assertEqual(result, expected)
