# -*- coding:utf-8 -*-
from common.cache.lru import LruCache


class TestLruCache:
    def test_get_and_set(self):
        cache = LruCache()
        assert cache.get("123") is None
        cache.set("name", "jack")
        assert cache.length() == 4
        assert cache.keys_count() == 1
        assert cache.capacity() == 100
        assert cache.get("name") == "jack"
        cache.reset_capacity(2)
        assert cache.get("name") is None
        assert cache.capacity() == 2
        assert cache.keys_count() == 0
        assert cache.length() == 0
        cache.add_capacity(10)
        cache.set("name", "jack")
        cache.set("age", "100")
        cache.set("gender", "man")
        assert cache.keys_count() == 2
        assert cache.length() == 9
        assert cache.capacity() == 12
        assert cache.get("name") is None
        assert cache.get("age") == "100"
        cache.sub_capacity(4)
        assert cache.capacity() == 8
        assert cache.length() == 3
        assert cache.keys_count() == 1
        assert cache.get("gender") is None
        assert cache.get("age") == "100"
