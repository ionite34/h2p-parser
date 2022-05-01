from unittest import TestCase
from h2p_parser import symbols


class TestSymbols(TestCase):
    def test_to_full_type_tag(self):
        short_type_tags = ['V', 'N', 'P', 'A', 'R']
        full_type_tags = ['VERB', 'NOUN', 'PRON', 'ADJ', 'ADV']
        for short, full in zip(short_type_tags, full_type_tags):
            self.assertEqual(full, symbols.to_full_type_tag(short))
        # Test for invalid type tag
        self.assertEqual(None, symbols.to_full_type_tag('X'))
