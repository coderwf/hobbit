# -*- coding:utf-8 -*-
from common.collections.link_list import LinkList


class LruItem:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class LruCache:
    def __init__(self, capacity=100):
        """

        :param capacity:
        """
        assert capacity > 0
        self._capacity = capacity
        # key-Item
        self._treasures = {}
        self._length = 0
        self._link = LinkList()
        self._key_count = 0

    def get(self, key):
        """
        根据key获得value,key必须实现了__len__方法
        :param key:
        :return: value
        """
        if key not in self._treasures:
            return None
        item = self._treasures.get(key)
        # 移到链表最后面
        self._link.remove(item)
        self._link.insert_tail(item)
        return item.value.value

    def set(self, key, value):
        """

        :param key: 必须实现__len__方法
        :param value:
        :return:
        """
        assert value is not None
        item = self._link.insert_value_tail(LruItem(key, value))
        self._treasures[key] = item
        self._key_count += 1
        self._length += len(key)
        self._fix_cache()
        return key

    def _fix_cache(self):
        """
        当缓存过大时,需要删除不常用缓存
        :return:
        """
        while self._length > self._capacity:
            lru_item = self._link.remove_head()
            item_key = lru_item.key
            self._treasures.pop(item_key)
            self._length -= len(item_key)
            self._key_count -= 1

    def reset_capacity(self, new_capacity):
        assert new_capacity > 0
        if new_capacity != self._capacity:
            self._capacity = new_capacity
            self._fix_cache()
        return self._capacity

    def add_capacity(self, adds):
        assert adds >= 0
        self._capacity += adds
        return self._capacity

    def sub_capacity(self, subs):
        assert subs >= 0
        self.reset_capacity(self._capacity - subs)

    def keys_count(self):
        return self._key_count

    def capacity(self):
        return self._capacity

    def __len__(self):
        return self._length

    def length(self):
        return self._length
