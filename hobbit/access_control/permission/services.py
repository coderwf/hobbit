# -*- coding:utf-8 -*-
import logging
from hobbit.access_control.permission.base import AbstractPermission, PermissionCheckRes


class PermissionManageService:
    """
    负责组装权限模块
    """
    identity_key_permission_class_map = {}

    def __init__(self):
        raise Exception("Can't declare a %s class obj" % __class__.__name__)

    @staticmethod
    def register(identity_key, permission_class):
        if identity_key in PermissionManageService.identity_key_permission_class_map:
            logging.warning("[PermissionManageService][register] identity_key:%s already registered", identity_key)
            return False
        if not issubclass(permission_class, AbstractPermission):
            logging.warning("[PermissionManageService][register] permission_class:%s is invalid permission class",
                            permission_class)
            return False
        logging.info("[PermissionManageService][register] register %s:%s", identity_key, permission_class.__name__)
        PermissionManageService.identity_key_permission_class_map[identity_key] = permission_class
        return True

    @staticmethod
    def unregister(identity_key):
        if identity_key not in PermissionManageService.identity_key_permission_class_map:
            logging.warning("[PermissionManageService][unregister] identity_key:%s is unregistered")
            return False
        logging.info("[PermissionManageService][unregister] unregister %s", identity_key)
        PermissionManageService.identity_key_permission_class_map.pop(identity_key, None)
        return True

    @staticmethod
    def modify(identity_key, new_permission_class):
        if identity_key not in PermissionManageService.identity_key_permission_class_map:
            logging.warning("[PermissionManageService][modify] identify_key:%s is unregistered")
            return False
        if not issubclass(new_permission_class, AbstractPermission):
            logging.warning("[PermissionManageService][modify] permission_class:%s is invalid permission class",
                            new_permission_class)
            return False
        old_permission_class = PermissionManageService.identity_key_permission_class_map.pop(identity_key)
        logging.info("[PermissionManageService][modify] modify %s:%s→%s", identity_key,
                     old_permission_class.__name__, new_permission_class.__name__)
        PermissionManageService.identity_key_permission_class_map[identity_key] = new_permission_class
        return True

    @staticmethod
    def get_registered_permission(identity_key):
        permission_class = PermissionManageService.identity_key_permission_class_map.get(identity_key, None)
        if permission_class:
            return PermissionCheckRes(success=True, data=permission_class)
        return PermissionCheckRes(success=False)


# 将该权限装载
def auto_register_permission(identity_key, overwrite=False):
    def wrapper(cls):
        if overwrite or not not hasattr(cls, "identity_key"):
            setattr(cls, "identity_key", identity_key)
        # 注册该权限
        PermissionManageService.register(getattr(cls, "identity_key"), cls)
        return cls
    return wrapper


class AccessControlService:
    def __init__(self, operator_id):
        self.operator_id = operator_id

    def _get_operator_info(self):
        pass

    def _get_operator_roles(self):
        pass

    def _get_role_permissions(self):
        pass

    @staticmethod
    def register_permission(identity_key, permission_class):
        return PermissionManageService.register(identity_key, permission_class)

    @staticmethod
    def unregister_permission(identity_key):
        return PermissionManageService.unregister(identity_key)

    @staticmethod
    def register_permissions(permissions_map: dict):
        """

        :param permissions_map:
        :return:
        """
        for identity_key, permission_class in permissions_map.items():
            if issubclass(permission_class, AbstractPermission):
                PermissionManageService.register(identity_key, permission_class)

    @staticmethod
    def unregister_permissions(identity_key_list: list):
        for identity_key in set(identity_key_list):
            PermissionManageService.unregister(identity_key)

    def _has_permission(self, permission_identity_key, user_obj, *args, **kwargs):
        """
          用户自定义的权限访问是否通过
        :param permission_identity_key:
        :param user_obj:
        :param args:
        :param kwargs:
        :return: PermissionCheckRes
        """
        check_permission_func = getattr(self, permission_identity_key, None)
        if check_permission_func:
            return check_permission_func(user_obj, *args, **kwargs)
        return PermissionCheckRes(success=False)

    def check_has_access(self, permission_identity_key, user_obj, *args, **kwargs):
        """
          1.是否可以通过用户自己定义的权限访问机制
          2.该权限模块是否已经加载
          3.该权限当前是否可以访问

            用户不通过此函数进行权限校验时,需要自行调用check_sys_access函数进行系统默认权限校验
        """
        permission_result = self._has_permission(permission_identity_key, user_obj, *args, **kwargs)
        if permission_result.success is False:
            return permission_result
        return self.check_sys_access(permission_identity_key, user_obj)

    @staticmethod
    def check_sys_access(permission_identity_key, user_obj, *args, **kwargs):
        permission_result = PermissionManageService.get_registered_permission(permission_identity_key)
        if permission_result.success is False:
            return permission_result
        return permission_result.data.has_permission(permission_identity_key, user_obj, *args, **kwargs)

    def check_has_role(self, role_id):
        pass

    def check_has_roles(self, role_ids):
        pass
