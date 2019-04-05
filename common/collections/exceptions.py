# -*- coding:utf-8 -*-


class UnBelongingException(Exception):
    """
    不属于某个集合中的元素
    """
    def __init__(self, arg=""):
        self.arg = arg

    def __str__(self):
        return self.arg

    def __repr__(self):
        return self.__str__()

