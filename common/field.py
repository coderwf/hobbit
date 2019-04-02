# -*- coding:utf-8 -*-
from django.db import models
from common.pycrypt import AESEncrypt, hash_encode


aes_encrypt = AESEncrypt()


class SensitiveField(models.TextField):
    description = "Sensitive"

    def __init__(self, *args, **kwargs):
        super(SensitiveField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, *args, **kwargs):
        v = models.TextField.to_python(self, value)
        success, v = aes_encrypt.decrypt_to_str(v)
        if success == 0:
            raise Exception("failed to decrypt")
        return v

    def get_prep_value(self, value):
        success, value = aes_encrypt.encrypt(value)
        if success == 0:
            raise Exception("failed to encrypt")
        return value


class EncryptedField(models.TextField):
    description = "Decrypted"

    def __init__(self, *args, **kwargs):
        super(EncryptedField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, *args, **kwargs):
        v = models.TextField.to_python(self, value)
        return v

    def get_prep_value(self, value):
        try:
            value = hash_encode(value, encoding="utf-8")
            return value
        except Exception as e:
            raise Exception("failed to encrypt")

