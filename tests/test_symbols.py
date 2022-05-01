import pytest

from h2p_parser import symbols

short_type_tags = ['V', 'N', 'P', 'A', 'R']
full_type_tags = ['VERB', 'NOUN', 'PRON', 'ADJ', 'ADV']


class Test:
    @pytest.mark.parametrize('short, full', zip(short_type_tags, full_type_tags))
    def test_to_full_type_tag(self, short, full):
        assert symbols.to_full_type_tag(short) == full

    def test_to_full_type_tag_invalid(self):
        # Test for invalid type tag
        assert symbols.to_full_type_tag('X') is None
