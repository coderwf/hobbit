# -*- coding:utf-8 -*-

from common.collections.exceptions import UnBelongingException
from common.collections.item import Item


class LinkList:
    """
       双向循环链表
    """
    def __init__(self):
        self._length = 0
        self._root = Item(belongs=self)
        self._root.prev_item = self._root
        self._root.next_item = self._root

    def insert_before(self, at_item: Item, item: Item):
        """
        插入一个新结点到某个结点之前
        :param at_item:
        :param item:
        :return:
        """
        if at_item.belongs != self:
            raise UnBelongingException()
        next_item = at_item
        prev_item = at_item.prev_item

        prev_item.next_item = item
        item.prev_item = prev_item
        next_item.prev_item = item
        item.next_item = next_item

        item.belongs = self
        self._length += 1
        return item
    
    def insert_value_before(self, at_item: Item, value):
        return self.insert_before(at_item, Item(value=value))
        
    def insert_after(self, at_item: Item, item: Item):
        if at_item.belongs != self:
            raise UnBelongingException()
        self.insert_before(at_item.next_item, item)
        return item
    
    def insert_value_after(self, at_item: Item, value):
        return self.insert_after(at_item, Item(value=value))
        
    def insert_head(self, item: Item):
        """
          插入头结点
        :param item:
        :return:
        """
        return self.insert_after(self._root, item)
    
    def insert_value_head(self, value):
        return self.insert_head(Item(value=value))
        
    def insert_tail(self, item: Item):
        """
         插入尾结点
        :param item:
        :return:
        """
        return self.insert_before(self._root, item)
    
    def insert_value_tail(self, value):
        return self.insert_tail(Item(value=value))
        
    def remove(self, item: Item):
        """
        删除某个结点
        :param item:
        :return:value
        """
        if item.belongs != self:
            raise UnBelongingException()
        if not (self._root == item):
            prev_item = item.prev_item
            next_item = item.next_item
            prev_item.next_item = next_item
            next_item.prev_item = prev_item
            item.prev_item = item.next_item = item.belongs = None
            self._length -= 1
        return item.value

    def remove_tail(self):
        if self._root.next_item == self._root:
            return None
        return self.remove(self._root.prev_item)

    def remove_head(self):
        if self._root.next_item == self._root:
            return None
        return self.remove(self._root.next_item)

    def head_item(self):
        """
        返回第一个结点
        :return:
        """
        if self._root.next_item == self._root:
            return None
        return self._root.next_item

    def head_value(self):
        """

        :return: 返回值为None可能是value是None,也可能是item为None
        """
        item = self.head_item()
        if not item:
            return None
        return item.value

    def tail_item(self):
        if self._root.next_item == self._root:
            return None
        return self._root.prev_item

    def tail_value(self):
        """

        :return: 返回值为None可能是value是None,也可能是item为None
        """
        item = self.tail_item()
        if not item:
            return None
        return item.value

    def length(self):
        return self._length

    def __len__(self):
        return self._length
