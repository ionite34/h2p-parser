import pytest
import h2p_parser.format_ph as ph

data_sds = [
    "HH AE1 M AA2 R K",
    "P ER0 S EH1 N T",
    "AO1",
    "P AA1 R K",
    "K AA1 N S OW0 L"
]
data_list = [
    ['HH', 'AE1', 'M', 'AA2', 'R', 'K'],
    ['P', 'ER0', 'S', 'EH1', 'N', 'T'],
    ['AO1'],
    ['P', 'AA1', 'R', 'K'],
    ['K', 'AA1', 'N', 'S', 'OW0', 'L']
]
data_invalid = [
    (1, TypeError),
    (1.0, TypeError),
    ([1], TypeError),
    ([[1.0], [1.0]], TypeError),
    ({"a": 1}, TypeError),
    (("A", "B"), TypeError),
    (None, None),
    ([None], None),
    ([[None], [None]], None),
    ([], None),
    ([[]], None)
]


# noinspection PyTypeChecker
@pytest.mark.parametrize("ph_sds, ph_list", zip(data_sds, data_list))
def test_to_sds(ph_sds, ph_list):
    # SDS -> SDS
    assert ph.to_sds(ph_sds) == ph_sds
    # List -> SDS
    assert ph.to_sds(ph_list) == ph_sds
    # Nested Lists -> SDS
    assert ph.to_sds([ph_list]) == ph_sds
    assert ph.to_sds([[ph_list]]) == ph_sds


@pytest.mark.parametrize("ph_sds, ph_list", zip(data_sds, data_list))
def test_to_list(ph_sds, ph_list):
    # SDS -> List
    assert ph.to_list(ph_sds) == ph_list
    # List -> List
    assert ph.to_list(ph_list) == ph_list
    # Nested Lists -> List
    assert ph.to_list([ph_list]) == ph_list
    assert ph.to_list([[ph_list]]) == ph_list


@pytest.mark.parametrize("source, expected", data_invalid)
def test_to_sds_invalid(source, expected):
    if expected is TypeError:
        with pytest.raises(TypeError):
            ph.to_sds(source)
    else:
        assert ph.to_sds(source) == expected


@pytest.mark.parametrize("source, expected", data_invalid)
def test_to_list_invalid(source, expected):
    if expected is TypeError:
        with pytest.raises(TypeError):
            ph.to_list(source)
    else:
        assert ph.to_list(source) == expected
