# -*- coding:utf-8 -*-
from common.collections.link_list import LinkList


class TestLinkList:
    def test_insert(self):
        linklist = LinkList()
        assert len(linklist) == 0
        assert linklist.length() == 0
        linklist.insert_value_head(1)
        linklist.insert_value_head(2)
        linklist.insert_value_tail(3)
        assert len(linklist) == 3
        assert linklist.head_value() == 2
        assert linklist.tail_value() == 3
        assert linklist.head_item().value == 2
        assert linklist.tail_item().value == 3
        linklist = LinkList()
        assert len(linklist) == 0
        assert linklist.length() == 0
        linklist.insert_value_tail(1)
        linklist.insert_value_tail(2)
        linklist.insert_value_tail(3)
        linklist.insert_value_head(4)
        assert len(linklist) == 4
        assert linklist.head_value() == 4
        assert linklist.tail_value() == 3
        assert linklist.head_item().value == 4
        assert linklist.tail_item().value == 3

    def test_remove(self):
        linklist = LinkList()
        ret = linklist.insert_value_tail(4)
        linklist.remove(ret)
        assert len(linklist) == 0
        assert linklist.remove_head() is None
        assert linklist.remove_tail() is None
        linklist.insert_value_tail(4)
        linklist.insert_value_tail(5)
        linklist.insert_value_head(3)
        assert linklist.remove_tail() == 5
        assert linklist.remove_head() == 3
        assert linklist.remove_head() == 4
        assert linklist.remove_tail() is None
        assert linklist.head_item() is None
        assert linklist.head_value() is None
        item = linklist.insert_value_head(10)
        linklist.insert_value_before(item, 12)
        assert linklist.head_value() == 12
        assert linklist.tail_value() == 10
        assert linklist.remove_tail() == 10
        assert linklist.remove_tail() == 12
        item = linklist.insert_value_tail(50)
        assert linklist.head_value() == linklist.tail_value() == 50
        linklist.insert_value_after(item, 100)
        assert linklist.head_value() == 50
        assert linklist.tail_value() == 100