import pytest
from h2p_parser import dict_cache


def test_dict_cache():
    # Create dict cache instance
    cache = dict_cache.DictCache()
    assert isinstance(cache, dict_cache.DictCache)


def test_dict_cache_add():
    cache = dict_cache.DictCache()
    # Add item to cache
    cache.add('JARL', 'Y AA1 R L')
    assert cache._cache['JARL'][0] == 'Y AA1 R L'
    assert cache.get('JARL') == ('Y AA1 R L', None, False)


def test_dict_cache_get():
    cache = dict_cache.DictCache()
    assert cache.get('JARL') is None
    cache.load()
    assert cache.get('JARL')[0] == 'Y AA1 R L'
