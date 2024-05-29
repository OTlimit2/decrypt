from xor_cipher import *

idc = XORCipher()

plaintext = '123456-XY-001'
print(f"{'*'*10} 加密算法测试 {'*'*10}")
print(f'原始数据: {plaintext}, 类型: 普通样品')
a11 = idc.encrypt(plaintext)
print(f'第一次加密后: {a11}, 长度: {len(a11)}')
a12 = idc.encrypt(a11)
print(f'第二次加密后: {a12}, 长度: {len(a12)}')
# b11 = idc.decrypt(a12)
# print(f'解密二次加密: {b11}')
# b12 = idc.decrypt(b11)
# print(f'解密一次加密：{b12}\n')