# -*- coding:utf-8 -*-
from common.crypto.pycrypt import hash_encode
"""
email注册激活找回密码等服务
"""


class EmailService:
    @staticmethod
    def register():
        email = ""
        expire_time = 2 * 24 * 60 * 60
        key = ""
        plain_token = email + str(expire_time)
        hash_token = hash_encode(plain_token, salt=key)
        activate_link = "https://www.hobbit.com/activate?hug=%s" % hash_token


    @staticmethod
    def activate():
        pass
