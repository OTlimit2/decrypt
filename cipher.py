from Crypto.Cipher import AES, DES
import base64
import random
import os

class AppCipher:

    def __init__(self, input_path, out_path='./output', keypath='./keys', cipher_type=0):
        self._inpath = input_path
        self._outpath = out_path
        self._keypath = keypath
        self._inpath_is_dir = False
        self._keypath_is_dir = False
        # 0 - 加密, 1 - 解密
        self._type = cipher_type

        self.check_path()
    
    def check_path(self):
        if not os.path.exists(self._inpath):
            raise ValueError("加/解密文件路径不存在!")
        if not os.path.exists(self._outpath):
            raise ValueError("输出文件路径不存在!")
        if not os.path.exists(self._keypath):
            raise ValueError("密钥文件路径不存在!")
        if os.path.isdir(self._inpath):
            self._inpath_is_dir = True
        if os.path.isdir(self._keypath):
            self._keypath_is_dir = True
    
    def setkey(self):
        self._key = []
        if not self._keypath_is_dir:
            self._suffix = bytes([0])
            with open(self._keypath, 'rb') as f:
                self._key.append(f.read())
        else:
            n_keys = len(os.listdir(self._keypath))
            key_index = random.sample(range(1, n_keys+1), 2)
            self._suffix = bytes(key_index) + bytes([2])
            for i in key_index:
                with open(os.path.join(self._keypath, str(i)), 'r') as f:
                    self._key.append(f.read())
    
    def getkey(self):
        self._key = []


    def setcipher(self):
        self._aes_cipher = AES.new(self._key[0])
        self._des_cipher = DES.new(self._key[-1][:8])
    
    
    def processing(self):
        if self._type == 0:
            self.encrypt(filename)
        else:
            self.decrypt(filename)
    
    def encrypt(self):
        if self._inpath_is_dir:
            with open(filename, 'r', encoding='utf-8') as f:
                text = f.read()
            self.setkey()
            self.setcipher()
            text = self.encrypt_text(text) + self._suffix
            with open(os.path.join(
                self._outpath, os.path.basename(filename) + '.e'
            ), 'wb') as f:
                f.write(text)
        else:
            for fn in os.listdir(filename):
                with open(os.path.join(filename, fn),
                    'r', encoding='utf-8') as f:
                    text = f.read()
                self.setkey()
                self.setcipher()
                text = self.encrypt_text(text) + self._suffix
                with open(os.path.join(
                    self._outpath, fn +'.e'
                ), 'wb') as f:
                    f.write(text)
    
    def encrypt_text(self, text):
        n_fill = 4 - (len(text) + 1) % 4
        if text.endswith('='):
            text += '+' * n_fill
        else:
            text += '=' * n_fill
        plaintext = text.encode('utf-32')
        plaintext = self._aes_cipher.encrypt(plaintext)
        plaintext = self._des_cipher.encrypt(plaintext)
        return plaintext
    
    def decrypt(self):
        if not self._inpath_is_dir:
            with open(filename, 'rb') as f:
                text = f.read()
            text = self.decrypt_text(text)
            with open(os.path.join(
                self._outpath, os.path.basename(filename) + '.d'
            ), 'w', encoding='utf-8') as f:
                f.write(text)
        else:
            for fn in os.listdir(filename):
                if not fn.endswith('.e'):
                    continue
                with open(os.path.join(filename, fn), 'r') as f:
                    text = f.read()
                text = self.decrypt_text(text)
                with open(os.path.join(
                    self._outpath, fn +'.d'
                ), 'wb') as f:
                    f.write(text)
    
    def decrypt_text(self, text, filename):
        n_keys = text[-1]
        if self._keypath_is_dir and n_keys != 0:
            raise ValueError("解密需要指定密钥文件而非密钥库!")
        if n_keys == 0:
            self.setkey()
            self.setcipher()
        plaintext = text[:-n_keys-1]
        self._key_index = [x for x in text[-n_keys-1:-1]]
        if n_chain == 0:
            plaintext = decrypt_chain(plaintext, 0)

        return plaintext.rstrip(text[-1])
