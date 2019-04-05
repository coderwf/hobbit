# -*- coding:utf-8 -*-


class Item:
    def __init__(self, prev_item=None, next_item=None, value=None, belongs=None):
        """

        :param prev_item: prev item
        :param next_item: next item
        :param value: stored value
        """
        self.prev_item = prev_item
        self.next_item = next_item
        self.value = value
        self.belongs = belongs
