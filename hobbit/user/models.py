# -*- coding:utf-8 -*-
from django.db import models
from common.field import EncryptedField


class UserInfo(models.Model):
    user_id = models.IntegerField(max_length=20, primary_key=True)
    user_password = EncryptedField(max_length=25)
    phone_number = models.IntegerField(max_length=11, null=True, unique=True)
    nick_name = models.TextField(verbose_name="nick name of user", max_length="30")
    user_name = models.TextField(verbose_name="name of user", max_length=30, null=True)
    user_age = models.SmallIntegerField(verbose_name="age of user", max_length=3, default=0)
    user_gender = models.SmallIntegerField(verbose_name="gender of user(0:secret,1:gentle,2:madam)",
                                           max_length=2, default=0)


