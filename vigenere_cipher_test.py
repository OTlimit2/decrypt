from vigenere_cipher import *

idc = VigenereCipher()

# plaintext = '123456-XY-001'
# print(f"{'*'*10} 加密算法测试 {'*'*10}")
# print(f'原始数据: {plaintext}, 类型: 普通样品')
# a11 = '123456-0I1S20715'
# print(f'第一次加密后: {a11}, 长度: {len(a11)}')
# a12 = '610802-781Z19T0116'
# print(f'第二次加密后: {a12}, 长度: {len(a12)}')
# b11 = idc.decrypt_second(a12)
# b11 = '123456-0N3D920145'
# print(f'解密二次加密: {b11}')
# b12 = idc.decrypt_first(b11)
# print(f'解密一次加密：{b12}\n')

result_second = input('输入第二次加密的结果：')
result_first = idc.decrypt_second(result_second)
print(f'解密第二次加密的结果为：{result_first}')
print(f'解密第一次加密的结果为：{idc.decrypt_first(result_first)}')





# idc.decrypt_merge_model('数据模板/国标点模板.xls', '数据模板/土壤模板.xlsx', 'output')
# # idc.decrypt_merge1('数据模板/国标点模板.xls', '数据模板/土壤模板.xlsx', 'output')
# idc.decrypt_merge2('数据模板/国标点模板.xls', '数据模板/农产品模板.xlsx', 'output')
