# -*- coding:utf-8 -*-


class PermissionCheckRes:
    def __init__(self, success=True, message="", data=None):
        self.success = success
        self.message = message
        self.data = data


class PermissionCheckResMessage:
    NO_PERMISSION = "对不起,您没有访问权限"
    CLOSED_PERMISSION = "此权限还未开放"


class AbstractPermission:
    """
    最基础的抽象权限类
    """
    identity_key = "permission_abstract"

    @staticmethod
    def has_permission(self, identity_key, user_obj, *args, **kwargs):
        """
        最基础的业务权限判断
        :param self:
        :param identity_key:
        :param user_obj:
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

