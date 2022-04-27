from unittest import TestCase
from h2p_parser.cmudictext import CMUDictExt


class TestCMUDictExt(TestCase):
    def setUp(self):
        pass

    def test_cmudict_ext(self):
        # Test all default initialization
        target = CMUDictExt()
        self.assertIsInstance(target, CMUDictExt)
