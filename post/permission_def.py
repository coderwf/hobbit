# -*- coding:utf-8 -*-
from access_control.permission.base import AbstractPermission, PermissionCheckRes


class PostPermission:
    can_operate_post_all = "can_operate_post_all"
    can_post_post_permission = "can_post_post_permission"
    can_delete_self_post_permission = "can_delete_self_post_permission"
    can_delete_post_permission = "can_delete_post_permission"
    can_view_post_permission = "can_view_post_permission"
    can_reply_post_permission = "can_reply_post_permission"
    can_modify_self_post_permission = "can_modify_self_post_permission"
    can_modify_post_permission = "can_modify_post_permission"
    can_rename_post_permission = "can_rename_post_permission"


class CanOperatePostAll(AbstractPermission):
    identity_key = "can_operate_post_all"

    def has_permission(self, *args, **kwargs):
        PermissionCheckRes(True)


class CanPostPostPermission(CanOperatePostAll):
    identity_key = "can_post_post_permission"


class CanDeleteSelfPostPermission(CanOperatePostAll):
    identity_key = "can_delete_self_post_permission"


class CanDeletePostPermission(CanOperatePostAll):
    identity_key = "can_delete_post_permission"


class CanViewPostPermission(CanOperatePostAll):
    identity_key = "can_view_post_permission"


class CanReplyPostPermission(CanOperatePostAll):
    identity_key = "can_reply_post_permission"


class CanModifySelfPostPermission(CanOperatePostAll):
    identity_key = "can_modify_self_post_permission"


class CanModifyPostPermission(CanOperatePostAll):
    identity_key = "can_modify_post_permission"


class CanRenamePostPermission(CanOperatePostAll):
    identity_key = "can_rename_post_permission"


class PostPermissionService:
    def __init__(self, operator_id):
        self.operator_id = operator_id
