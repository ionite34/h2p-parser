from h2p_parser.compat import cmudict


def test_cmudict():
    # Create instance
    d = cmudict.CMUDict()
    assert isinstance(d, cmudict.CMUDict)
    assert isinstance(d.dict, dict)
