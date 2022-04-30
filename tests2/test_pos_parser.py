import pytest

import h2p_parser.pos_parser as pos_parser


verb_pos_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
noun_pos_tags = ['NN', 'NNS', 'NNP', 'NNPS']
adverb_pos_tags = ['RB', 'RBR', 'RBS']

testdata = []

for test_tag in verb_pos_tags:
    testdata.append((test_tag, 'VERB'))
for test_tag in noun_pos_tags:
    testdata.append((test_tag, 'NOUN'))
for test_tag in adverb_pos_tags:
    testdata.append((test_tag, 'ADVERB'))


class Test:
    @pytest.mark.parametrize('tag, expected', testdata)
    def test_get_parent_pos_verb(self, tag, expected):
        actual = pos_parser.get_parent_pos(tag)
        assert actual == expected

    def test_get_parent_pos_invalid_tag(self):
        # If the pos tag is not in the list, expect None
        assert pos_parser.get_parent_pos('XYZ') is None
