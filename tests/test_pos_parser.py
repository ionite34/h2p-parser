from unittest import TestCase
import pos_parser


class Test(TestCase):
    def test_get_parent_pos(self):
        # Create a list of verb pos tags
        verb_pos_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        # Create a list of noun pos tags
        noun_pos_tags = ['NN', 'NNS', 'NNP', 'NNPS']

        # Loop for each verb pos tag
        for verb_pos_tag in verb_pos_tags:
            actual = pos_parser.get_parent_pos(verb_pos_tag)
            assert actual == 'VERB'

        # Loop for each noun pos tag
        for noun_pos_tag in noun_pos_tags:
            actual = pos_parser.get_parent_pos(noun_pos_tag)
            assert actual == 'NOUN'

        # If the pos tag is not in the list, expect None
        assert pos_parser.get_parent_pos('XYZ') is None
