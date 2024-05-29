from datetime import date
from os import path
import os
import random
import string
import shutil

class KeyRepo:

    def __init__(self, repo_path='./keys', n_keys=50):
        if not path.exists(repo_path):
            os.makedirs(repo_path)
        self._repo_path = repo_path
        self._n_keys = n_keys
    
    def backup(self):
        i = 0
        backup_dir = self._repo_path + '_' + date.today().strftime('%d_%m_%Y')
        while path.isdir(backup_dir + '_' + str(i)):
            i += 1
        backup_dir = backup_dir + '_' + str(i)
        shutil.move(self._repo_path, backup_dir)
        os.mkdir(self._repo_path)
    
    def clear(self):
        shutil.rmtree(self._repo_path)
        os.mkdir(self._repo_path)

    def gen(self, length = 16):
        for i in range(1, self._n_keys+1):
            with open(path.join(self._repo_path, str(i)), 'w') as f:
                random_str = ''.join(random.choices(
                    string.ascii_letters + string.digits, k=length
                ))
                f.write(random_str)
    
    def gen_vigenere(self, ab_length = 2, num_length = 3):
        for i in range(1, self._n_keys+1):
            with open(path.join(self._repo_path, str(i)), 'w') as f:
                random_str = ''.join(random.choices(string.ascii_uppercase, k=ab_length))
                random_str += ''.join(random.choices(string.digits, k=num_length))
                f.write(random_str)
