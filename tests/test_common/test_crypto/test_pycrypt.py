# -*- coding:utf-8 -*-
from common.crypto.pycrypt import hash_encode, random_str, PaddingEncoding, AESEncrypt


class TestPyCrypt:
    def test_hash_encode(self):
        assert len(hash_encode("i love you", "111", encoding="gbk")) == 32
        assert len(hash_encode("i love you", "111", encoding="utf-8")) == 32
        assert len(hash_encode("i love you", "111", encoding=None)) == 32
        assert len(hash_encode("i love you", "111",)) == 32
        assert len(hash_encode(dict(success=True), "111", encoding="gbk")) == 32
        assert len(hash_encode([1, 2, 4], "111", encoding="gbk")) == 32

    def test_random_str(self):
        assert len(random_str(100)) == 100
        assert len(random_str(20)) == 20
        assert len(random_str(10)) == 10
        assert len(random_str(20, encoding="utf-8")) == 20

    def test_padding_encoding(self):
        pe = PaddingEncoding(32)
        str1 = "i love you"
        e_str1 = pe.encode_str(str1)
        assert pe.decode_str(e_str1) == str1
        assert str1 == pe.decode_bytes(pe.encode_str(str1, output_encoding="gbk")).decode("gbk")
        assert pe.decode_bytes(pe.encode_bytes(str1.encode("utf-8"), "utf-8", "gbk")) == str1.encode("gbk")

    def test_aes_encrypt(self):
        aes = AESEncrypt()
        str1 = "hey boy"
        success, e_str1 = aes.encrypt(str1)
        assert success == 1
        success, res = aes.decrypt_to_str(e_str1, encoding="utf-8")
        assert success == 1
        assert res == str1
