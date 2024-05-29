from base64 import b64encode, b64decode
from os import path
import random
import os

class XORCipher:

    def __init__(self, key_repo='./keys', _sample_type='普通样品'):
        if not path.isdir(key_repo):
            raise ValueError("密钥库路径错误!")
        self._key_repo = key_repo
        self._sample_type = _sample_type
        self._n_keys = len(os.listdir(key_repo))

    def _set_type(self):
        """设置样品类型"""
        if self._sample_type == '普通样品':
            self._type = '1'
        elif self._sample_type == '标准样品':
            self._type = '2'
        elif self._sample_type == '互检样品':
            self._type = '3'
        elif self._sample_type == '平行样品':
            self._type = '4'
        else:
            self._type = '0'

    def _set_encryt_key(self):
        """选择加密密钥"""
        key_ind = random.randint(1, self._n_keys)
        self._keyfile = format(key_ind, '02x')
        with open(path.join(self._key_repo, str(key_ind)), 'r') as f:
            self._key = f.read()

    def _get_decrypt_key(self):
        """获取解密密钥"""
        key_ind = int(self._keyfile, 16)
        with open(path.join(self._key_repo, str(key_ind)), 'r') as f:
            self._key = f.read()
    
    def encrypt(self, plaintext):
        """加密过程"""
        prefix = plaintext[:7]
        self._set_encryt_key()
        self._set_type()
        encrypted = bytes_xor(plaintext[7:], self._key)
        encrypted = bytes(encrypted, encoding = 'ascii')
        print(encrypted)
        encrypted = b64encode(encrypted).decode('ascii')
        return prefix + encrypted + self._type + self._keyfile

def bytes_xor(s1, s2):
    """按位异或s1 s2"""
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))