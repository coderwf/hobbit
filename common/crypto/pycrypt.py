# -*- coding:utf-8 -*-
import json
import base64
import string
import hashlib
import random
from Crypto.Cipher import AES


def hash_encode(data, salt: str = "", encoding=None):
    """
    对data进行md5加密
    :param data: 需要进行编码的数据
    :param salt: 加盐key
    :param encoding:是否返回encoding后的数据
    :return: str
    """
    if isinstance(data, (dict, list)):
        pre_data = json.dumps(data)
    elif isinstance(data, str):
        pre_data = data
    else:
        raise TypeError("data for encode must be (str, dict, list)")
    if not encoding:
        return hashlib.md5((pre_data+salt).encode(encoding="utf-8")).hexdigest()
    return hashlib.md5((pre_data+salt).encode(encoding="utf-8")).hexdigest().encode(encoding=encoding)


def random_str(num: int, encoding=None):
    """
    随机生成num位字符串
    :param num: 生成字符串个数
    :param encoding: 是否进行编码
    :return:
    """
    assert num > 0
    source = string.digits + string.ascii_letters
    res = ""
    for i in range(num):
        res += source[random.randint(0, len(source) - 1)]
    if not encoding:
        return res
    return res.encode(encoding=encoding)


class PaddingEncoding:
    """
    按照block_size进行位补充
    """
    def __init__(self, block_size):
        self.block_size = block_size

    def _padding_data(self, data):
        data_length = len(data)
        amount_to_pad = self.block_size - (data_length % self.block_size)
        if amount_to_pad == 0:
            amount_to_pad = self.block_size
        return amount_to_pad * chr(amount_to_pad)

    def encode_bytes(self, data: bytes, encoding, output_encoding=True):
        """
        对bytes类型进行补位
        :param data:
        :param encoding: bytes的encoding类型
        :param output_encoding:返回数据是否进行编码
        :return: bytes or str
        """
        if not isinstance(data, bytes):
            raise TypeError("data must be bytes type")
        padding_data = self._padding_data(data).encode(encoding)
        if output_encoding:
            return data + padding_data
        return (data + padding_data).decode(encoding)

    def encode_str(self, data, output_encoding=None):
        """

        :param data:
        :param output_encoding: 返回数据是否进行编码
        :return:
        """
        if not isinstance(data, (str, list, dict)):
            raise TypeError("data must be (str, dict, list) type")
        pre_data = data
        if not isinstance(data, str):
            pre_data = json.dumps(data)
        padding_data = self._padding_data(pre_data)
        if not output_encoding:
            return pre_data + padding_data
        return (pre_data + padding_data).encode(encoding=output_encoding)

    def decode_bytes(self, data: bytes):
        """

        :param data:
        :return: bytes
        """
        if not isinstance(data, bytes):
            raise TypeError("data must be bytes type")
        amount_to_pad = data[-1]
        if amount_to_pad < 1 or amount_to_pad > self.block_size:
            amount_to_pad = 0
        return data[:-amount_to_pad]

    def decode_str(self, data: str, output_encoding=None):
        if not isinstance(data, str):
            raise TypeError("data must be str type")
        amount_to_pad = ord(data[-1])
        if amount_to_pad < 1 or amount_to_pad > self.block_size:
            amount_to_pad = 0
        if not output_encoding:
            return data[:-amount_to_pad]
        return data[:-amount_to_pad].encode(encoding=output_encoding)


class AESEncrypt:
    def __init__(self, salt="1234567890085438", url_safe=False):
        """

        :param salt: 加盐
        :param url_safe
        """
        assert len(salt) in (16, 24, 32)
        self.salt = salt
        self.mode = AES.MODE_CBC
        self.url_safe = url_safe
        self.pe = PaddingEncoding(AES.block_size)

    def encrypt(self, text, encoding="utf-8"):
        """
        对明文进行加密
        :param text:待加密的明文
        :param encoding:编码方式
        :return:bytes
        """
        """
        如果text为str则需要指定编码方式,如果test为bytes也需要指明编码方式
        """
        if not isinstance(text, (bytes, str, dict, list)):
            raise TypeError("test must be (bytes, str, dict, list) type")
        if isinstance(text, bytes):
            padding_text = self.pe.encode_bytes(text, encoding=encoding, output_encoding=True)
        else:
            pre_text = text
            if isinstance(text, (dict, list)):
                pre_text = json.dumps(text)
            padding_text = self.pe.encode_str(pre_text, output_encoding=encoding)
        # 再添加16位长度的随机字符串到待加密字符串开头
        padding_text = random_str(AES.block_size, encoding=encoding) + padding_text
        try:
            aes = AES.new(self.salt, self.mode, self.salt[:AES.block_size])
            encrypted_text = aes.encrypt(padding_text)
            # 用base64编码
            if self.url_safe:
                return 1, base64.urlsafe_b64encode(encrypted_text)
            return 1, base64.b64encode(encrypted_text)
        except Exception as e:
            return 0, None

    def decrypt_to_json_decoder(self, encrypted: bytes, encoding="utf-8"):
        success, origin_text = self.decrypt_to_str(encrypted, encoding)
        if success == 0:
            return success, None
        if not origin_text:
            return success, origin_text
        dict_content = json.loads(origin_text)
        return success, dict_content

    def decrypt_to_str(self, encrypted: bytes, encoding="utf-8"):
        success, origin_text = self.decrypt(encrypted)
        if success == 0:
            return success, None
        return success, origin_text.decode(encoding=encoding)

    def decrypt(self, encrypted: bytes):
        """
        解密加密的数据
        :param encrypted:
        :param encoding:
        :return:
        """
        if not isinstance(encrypted, bytes):
            raise TypeError("encrypted text must be bytes")
        try:
            # base64解码
            if self.url_safe:
                aes_text = base64.urlsafe_b64decode(encrypted)
            else:
                aes_text = base64.b64decode(encrypted)

            # AES-CBC解密
            aes = AES.new(self.salt, self.mode, self.salt[:AES.block_size])
            plain_text = aes.decrypt(aes_text)

            # 去掉开头的随机字符串
            plain_text = plain_text[AES.block_size:]

            # 去掉填充位
            origin_text = self.pe.decode_bytes(plain_text)
            return 1, origin_text
        except Exception as e:
            return 0, None



