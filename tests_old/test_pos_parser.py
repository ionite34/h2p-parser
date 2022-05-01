from unittest import TestCase
import h2p_parser.pos_parser as pos_parser


class Test(TestCase):
    def test_get_parent_pos(self):
        # Create a list of verb pos tags
        verb_pos_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        # Create a list of noun pos tags
        noun_pos_tags = ['NN', 'NNS', 'NNP', 'NNPS']
        # Create a list of adverb pos tags
        adverb_pos_tags = ['RB', 'RBR', 'RBS']

        # Loop for each verb pos tag
        for verb_pos_tag in verb_pos_tags:
            actual = pos_parser.get_parent_pos(verb_pos_tag)
            self.assertEqual('VERB', actual)

        # Loop for each noun pos tag
        for noun_pos_tag in noun_pos_tags:
            actual = pos_parser.get_parent_pos(noun_pos_tag)
            self.assertEqual('NOUN', actual)

        # Loop for each adverb pos tag
        for adverb_pos_tag in adverb_pos_tags:
            actual = pos_parser.get_parent_pos(adverb_pos_tag)
            self.assertEqual('ADVERB', actual)

        # If the pos tag is not in the list, expect None
        self.assertIsNone(pos_parser.get_parent_pos('XYZ'))
