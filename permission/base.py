# -*- coding:utf-8 -*-


class AbstractPermission:
    """
    最基础的抽象权限类
    """
    def __init__(self, operator_id):
        self.operator_id = operator_id

    def has_permission(self):
        pass
    