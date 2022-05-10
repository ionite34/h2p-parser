import pytest
import uuid
import os
from h2p_parser import dict_cache
from h2p_parser import DATA_PATH

test_f1 = f'temp_{uuid.uuid4()}.db'
test_f2 = f'temp_{uuid.uuid4()}.db'
test_f3 = f'temp_{uuid.uuid4()}.db'
test_exp = f'temp_{uuid.uuid4()}.dict'


# Fixture to remove temp db files
@pytest.fixture(scope='session')
def clear_files_teardown(request):
    yield None
    # Remove the requested file
    print(f'Removing {request.param}')
    with DATA_PATH.joinpath(request.param) as f:
        os.remove(f)
        assert not os.path.exists(f)


def test_dict_cache():
    # Create dict cache instance
    cache = dict_cache.DictCache()
    assert isinstance(cache, dict_cache.DictCache)


@pytest.mark.parametrize('clear_files_teardown', [test_f1], indirect=True)
def test_dict_cache_add(clear_files_teardown):
    cache = dict_cache.DictCache(test_f1)
    # Add item to cache
    cache.add('JARL', 'Y AA1 R L')
    assert cache._cache['JARL'][0] == 'Y AA1 R L'
    assert cache.get('JARL') == ('Y AA1 R L', None, False)


@pytest.mark.parametrize('clear_files_teardown', [test_f1], indirect=True)
def test_dict_cache_get(clear_files_teardown):
    cache = dict_cache.DictCache(test_f1)
    cache.add('ALTA', 'AA1 L T AH0')
    assert cache.get('ALTA') == ('AA1 L T AH0', None, False)
    cache.save()
    # Load new cache
    cache2 = dict_cache.DictCache(test_f1)
    cache2.load()
    assert len(cache2._cache) == 1
    assert cache2.get('ALTA') == ('AA1 L T AH0', None, False)


# Test for clear and check_clear
@pytest.mark.parametrize('clear_files_teardown', [test_f2], indirect=True)
def test_clear(clear_files_teardown):
    # Create a new db
    cache = dict_cache.DictCache(test_f2)
    # Add items
    cache.add('TEST', 'T EH1 S T')
    cache.add('ALRIGHT', 'AO2 L R AY1 T')
    cache.save()
    # Check clear, 2/2 entries should be affected
    assert cache.check_clear() == (2, 2)
    # Set one entry to checked state
    cache.add('TEST', 'T EH1 S T', checked=True)
    cache.save()
    # Check clear, 1/2 entries should be affected
    assert cache.check_clear() == (1, 2)


@pytest.mark.parametrize('clear_files_teardown', [test_f3], indirect=True)
def test_export(clear_files_teardown):
    # Create a new db
    cache = dict_cache.DictCache(test_f3)
    # Add some items
    cache.add('TEST', 'T EH1 S T', checked=True)
    cache.add('ALRIGHT', 'AO2 L R AY1 T')
    cache.add('ALTA', 'AA1 L T AH0', checked=True)
    cache.save()
    # Export to file
    with DATA_PATH.joinpath(test_exp) as f:
        try:
            cache.export(f)
            assert os.path.exists(f)
            # Test read
            with open(f, 'r') as rd_f:
                lines = rd_f.readlines()
                assert len(lines) == 2
                assert lines[0].strip() == 'TEST  T EH1 S T'
                assert lines[1].strip() == 'ALTA  AA1 L T AH0'
        finally:
            os.remove(f)
