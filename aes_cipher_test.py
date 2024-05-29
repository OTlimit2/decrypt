from aes_cipher import *

idc = AESCipher()
# plaintext = '123456-XY-001'
# print('********** 加密算法测试 **********')
# print(f'    原始数据: {plaintext}, 类型: 普通样品')
# a11 = idc.encrypt(plaintext)
# print(f'第一次加密后: {a11}, 长度: {len(a11)}')
# a12 = idc.encrypt(a11)
# print(f'第二次加密后: {a12}, 长度: {len(a12)}')
# b11 = idc.decrypt(a12)
# print(f'解密二次加密: {b11}')
# b12 = idc.decrypt(b11)
# print(f'解密一次加密：{b12}\n')


print('********** WEB密文解密测试 **********')
ciphertext_1 = '12sMIGI9ovb070Xiv42UAnIg==11c'
print(f'WEB第一次加密结果：{ciphertext_1}')
ciphertext_2 = '12t3riPecTjItX8NWzJSXM/gPW9MXOZ81wQT9phdMnuqw=124'
print(f'WEB第一次解密结果：{ciphertext_2}')
decrypted_2 = idc.decrypt(ciphertext_2)
print(f'第一次解密结果：{decrypted_2}')
decrypted_1 = idc.decrypt(decrypted_2)
print(f'第二次解密结果：{decrypted_1}')
