from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from os import path
import random
import os

class AESCipher:

    def __init__(self, key_repo='./keys', sample_type='普通样品', iv='1234567812345678'):
        if not path.isdir(key_repo):
            raise ValueError("密钥库路径错误!")
        self._key_repo = key_repo
        self._sample_type = sample_type
        self._iv = iv
        self._n_keys = len(os.listdir(key_repo))
        self._set_type()
    
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
    
    def _set_encrypt_cipher(self):
        """设置加密器"""
        # 从密钥库中选取密钥
        key_ind = random.randint(1, self._n_keys)
        with open(path.join(self._key_repo, str(key_ind)), 'r') as f:
            key = f.read()

        # 将密钥信息作为加密结果后缀
        self._keyfile = format(key_ind, '02x')
        # 获取 AES
        self._cipher = AES.new(key=key, mode=2, IV=self._iv)
    
    def _set_decrypt_cipher(self):
        """设置解密器"""
        key_ind = int(self._keyfile, 16)
        with open(path.join(self._key_repo, str(key_ind)), 'r') as f:
            key = f.read()
        self._cipher = AES.new(key=key, mode=2, IV=self._iv)
    
    def encrypt(self, plaintext):
        """加密过程"""
        prov = plaintext[:2]
        self._set_encrypt_cipher()
        self._set_type()
        pad_ = lambda s: s + (16 - len(s) % 16) * '\0'
        plaintext = pad_(plaintext)
        encrypted = self._cipher.encrypt(plaintext)
        encrypted = b64encode(encrypted).decode('ascii')
        return prov + encrypted + self._type + self._keyfile

    def decrypt(self, text):
        """解密过程"""
        text, self._keyfile = text[2:-3], text[-2:]
        self._set_decrypt_cipher()
        decrypted = self._cipher.decrypt(b64decode(text))
        decrypted = decrypted.rstrip(bytes([decrypted[-1]]))
        return decrypted.decode('ascii')
    