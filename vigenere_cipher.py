from os import path
from collections import OrderedDict
import xlrd
import openpyxl
import string
import random
import os


class VigenereCipher:

    def __init__(self, key_repo='./keys_vigenere', _sample_type='普通样品'):
        if not path.isdir(key_repo):
            raise ValueError("密钥库路径错误!")
        self._key_repo = key_repo
        self._sample_type = _sample_type
        self._n_keys = len(os.listdir(key_repo))
        self.DIANWEI=20
        self.ZHONGJINSHU=10
        self.NONGCHANPIN=8
        self.NONGYAO=23
        self.LIHUA=19

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

    def _get_type(self, type_str):
        """获取样品类型"""
        if type_str == '01':
            self._sample_type == '普通样品'
        elif type_str == '02':
            self._sample_type == '互检样品'
        elif type_str == '03':
            self._sample_type == '平行样品'
        else:
            self._sample_type == '标准样品'

    def _set_encryt_key(self):
        """选择加密密钥"""
        key_ind = random.randint(1, self._n_keys)
        self._keyfile = format(key_ind, '02x')
        with open(path.join(self._key_repo, str(key_ind)), 'r') as f:
            self._key = f.read()

    def _get_decrypt_key(self, key_str):
        """获取解密密钥"""
        key_ind = int(key_str)
        with open(path.join(self._key_repo, str(key_ind)), 'r') as f:
            self._key = f.read()

    def encrypt(self, plaintext):
        """加密过程"""
        pass

    def decrypt_first(self, ciphertext):
        """解密过程"""
        prefix = ciphertext[:7]
        self._get_decrypt_key(ciphertext[-2:])
        self._get_type(ciphertext[-4:-2])
        alphabet, nums = self._get_alphabet_nums(ciphertext[7:-4])
        alphabet = self.vigenere_decrypt_alphabet(alphabet)
        nums = self.vigenere_decrypt_nums(nums)
        return ''.join([prefix, alphabet, '-', nums])

    def decrypt_second(self, ciphertext):
        """解密过程
            150421-3Q79M020323
        """
        prefix = ciphertext[:7]                 # 150421-
        self._get_decrypt_key(ciphertext[-2:])  # 23
        self._get_type(ciphertext[-4:-2])       # 03
        alphabet, nums = self._get_alphabet_nums(ciphertext[7:-4]) # 3Q79M02
        alphabet = self.vigenere_decrypt_alphabet(alphabet)
        nums = self.vigenere_decrypt_nums(nums)
        plaintext = ''.join([nums[0], alphabet[0], nums[1], alphabet[1], nums[2:-2]])
        return ''.join([prefix, plaintext, ciphertext[-4:-2], nums[-2:]])

    def _get_alphabet_nums(self, text):
        """获取密文中字母和数字部分"""
        alphabet = ""
        nums = ""
        for c in text:
            if c in string.ascii_letters:
                alphabet += c
            elif c in string.digits:
                nums += c
        return alphabet, nums

    def vigenere_decrypt_alphabet(self, ciphertext):
        """维吉尼亚密码解码字母部分"""
        key = self._key[:2]
        text_len = len(ciphertext)
        key_len = len(key)
        plaintext = ""

        for i in range(text_len):
            offset = ord(key[i % key_len]) - ord('A') + 1
            c = ord(ciphertext[i]) - offset
            if c < ord('A'):
                c += 26
            plaintext += chr(c)

        return plaintext

    def vigenere_decrypt_nums(self, ciphertext):
        """维吉尼亚密码解码数字部分"""
        key = self._key[2:]
        text_len = len(ciphertext)
        key_len = len(key)
        plaintext = ""

        for i in range(text_len):
            offset = ord(key[i % key_len]) - ord('0') + 1
            c = ord(ciphertext[i]) - offset
            if c < ord('0'):
                c += 10
            plaintext += chr(c)

        return plaintext
    
    def is_number(self,s):
        '''
        判断是否为数字
        '''
        try:
            float(s)
            return True
        except ValueError:
            pass
 
        return False

    def parallel_sample(self, values, cur_row, start_point, num):
        """
        平行样本处理，2020.3.28
        """
        j = 1
        for i in range(start_point, start_point+num):
            if self.is_number(values[i]) and self.is_number(cur_row[j]):
                values[i] = str((float(values[i])+float(cur_row[j]))/2)
            if not self.is_number(values[i]) and self.is_number(cur_row[j]):
                values[i] = cur_row[j]
            j += 1
        return values

    # def parallel_sample(self, values, cur_row, start_point, num):
    #     """
    #     平行样本处理，2020.3.28
    #     """
    #     j = 1
    #     for i in range(start_point, start_point+num):
    #         if values[i] != '' and cur_row[j] != '':
    #             values[i] = str((float(values[i])+float(cur_row[j]))/2)
    #         if values[i] == '' and cur_row[j] != '':
    #             values[i] = cur_row[j]
    #         j += 1
    #     return values

    def parallel(self,table_dict,table,colum1,colum2):
        """
        平行样处理
        """
        para = OrderedDict()
        for irow in range(1, table.nrows):
            cur_row = table.row_values(irow)
            cipher_1 = self.decrypt_second(cur_row[0])
            cur_id = self.decrypt_first(cipher_1)
            front_len = self.DIANWEI + colum1
            if cur_id in table_dict:
                if cur_id in para.keys():
                    dict_len = len(table_dict[cur_id])
                    if dict_len < front_len + colum2:  # 字段数不够
                        add = ['' for x in range(front_len + colum2 - dict_len)]
                        table_dict[cur_id] += add
                    table_dict[cur_id] = self.parallel_sample(table_dict[cur_id], cur_row, front_len, colum2)
                    para[cur_id] += 1
                else:
                    length = len(table_dict[cur_id])
                    if length < front_len: 
                        add = ['' for x in range(front_len - length)]
                        table_dict[cur_id] += add
                    para[cur_id] = 1
                    table_dict[cur_id] += cur_row[1:]
        return table_dict


    def no_parallel(self,table_dict,table,column_num):
        """
        非平行样处理
        """
        for irow in range(1, table.nrows):
            cur_row = table.row_values(irow)
            cipher_1 = self.decrypt_second(cur_row[0])
            cur_id = self.decrypt_first(cipher_1)
            if cur_id in table_dict:
                length = len(table_dict[cur_id])
                if length < column_num: 
                    add = ['' for x in range(column_num - length)]
                    table_dict[cur_id] += add
                table_dict[cur_id] += cur_row[1:]
        return table_dict


    def table_save(self, new_table, outpath, filename):
        """
        文件保存
        """
        workbook = openpyxl.Workbook()
        sheet = workbook['Sheet']
        for irow in range(len(new_table)):
            for icol in range(len(new_table[irow])):
                sheet.cell(row=irow+1, column=icol+1).value = new_table[irow][icol]
        workbook.save(os.path.join(outpath, filename))


    def decrypt_merge_model(self, fp1, fp2, fp3, fp4, fp5 , outpath):
        """
        文件合并逻辑:
          fp1 模板文件
          fp2 土壤重金属文件
          fp3 农产品文件
          fp4 土壤农药
          fp5 土壤理化
        """
        # excel fields
        field_1 = ['当前点位编码', '初始点位编码', '采样年份','任务类型', '省', '市', '县', '乡/镇', '村', '行政区划', '组',
                   '东经', '北纬', '海拔高度', '土地利用方式', '土类名称', '亚类名称', '成土母质', '主产农作物_1', '主产农作物_2']
        # field_2 = ['有机质', 'As', 'Cd', 'Cr', 'Cu', 'Hg', 'Ni', 'Pb', 'Zn']
        # field_3 = ['农产品As', '农产品Cd', '农产品Cr', '农产品Hg', '农产品Pb', '农产品Cu', '农产品Zn', '农产品Ni']
        # field_4 = ['六六六','滴滴涕','毒死蜱','三唑磷','氯氰菊酯','氯氟氰菊酯','氰戊菊酯','氯虫苯甲酰胺','噻虫啉',
        #            '哒螨灵','吡虫啉','三环唑','己唑醇','戊唑醇','多菌灵','百菌清','苯醚甲环唑','烯酰吗啉','嘧菌酯','稻瘟灵','乙草胺','丁草胺','锈去津']
        # field_5 = ['土壤pH','阳离子交换量','土壤粘粒','土壤粉粒','土壤砂粒','全氮','有效磷','速效钾','缓效钾','有效硼',
        #            '有效钼','有效铜','有效硅','有效锰','有效铁','有效硫','交换性钙','交换性镁','水分','有效锌']

        # 两文件合并逻辑
        if fp2 and not fp3 and not fp4 and not fp5:     # 模板+土壤重金属
            self.decrypt_merge2(fp1, fp2, field_1, outpath, self.ZHONGJINSHU)
        if not fp2 and fp3 and not fp4 and not fp5:     # 模板+农产品
            self.decrypt_merge2(fp1, fp3, field_1, outpath, self.NONGCHANPIN)
        if not fp2 and not fp3 and fp4 and not fp5:     # 模板+土壤农药
            self.decrypt_merge2(fp1, fp4, field_1, outpath)
        if not fp2 and not fp3 and not fp4 and fp5:     # 模板+土壤理化
            self.decrypt_merge2(fp1, fp5, field_1, outpath, self.LIHUA)
        
        # 三文件合并逻辑
        if fp2 and fp3 and not fp4 and not fp5:                                             # 模板+重金属+农产品
            self.decrypt_merge3(fp1, fp2, fp3, field_1, outpath, self.ZHONGJINSHU, self.NONGCHANPIN)
        if fp2 and not fp3 and fp4 and not fp5:                                             # 模板+重金属+农药
            self.decrypt_merge3(fp1, fp2, fp4, field_1, outpath, self.ZHONGJINSHU)
        if fp2 and not fp3 and not fp4 and fp5:                                             # 模板+重金属+理化
            self.decrypt_merge3(fp1, fp2, fp5, field_1, outpath, self.ZHONGJINSHU, self.LIHUA)
        if not fp2 and fp3 and fp4 and not fp5:                                             # 模板+农产品+农药
            self.decrypt_merge3(fp1, fp3, fp4, field_1, outpath, self.NONGCHANPIN)
        if not fp2 and fp3 and not fp4 and fp5:                                             # 模板+农产品+理化
            self.decrypt_merge3(fp1, fp3, fp5, field_1, outpath, self.NONGCHANPIN, self.LIHUA)
        if not fp2 and not fp3 and fp4 and fp5:                                             # 模板+理化+农药
            self.decrypt_merge3(fp1, fp5, fp4, field_1, outpath, self.LIHUA)

        # 四文件合并逻辑
        if fp2 and fp3 and fp4 and not fp5:                                                 # 模板+农产品+重金属+农药
            self.decrypt_merge4(fp1,fp3,fp2,fp4,field_1,outpath,self.NONGCHANPIN,self.ZHONGJINSHU)
        if fp2 and fp3 and not fp4 and fp5:                                                 # 模板+农产品+重金属+理化
            self.decrypt_merge4(fp1,fp3,fp2,fp5,field_1,outpath,self.NONGCHANPIN,self.ZHONGJINSHU,self.LIHUA)
        if fp2 and not fp3 and fp4 and fp5:                                                 # 模板+重金属+理化+农药
            self.decrypt_merge4(fp1,fp2,fp5,fp4,field_1,outpath,self.ZHONGJINSHU,self.LIHUA)
        if not fp2 and fp3 and fp4 and fp5:                                                 # 模板+农产品+理化+农药
            self.decrypt_merge4(fp1,fp3,fp5,fp4,field_1,outpath,self.NONGCHANPIN,self.LIHUA)
        
        # 五文件合并逻辑
        if fp2 and fp3 and fp4 and fp5:                                                     # 模板+农产品+重金属+理化+农药
            self.decrypt_merge_all(fp1, fp3, fp2, fp5, fp4, field_1, outpath, self.NONGCHANPIN, self.ZHONGJINSHU, self.LIHUA)

    def decrypt_merge2(self, fp1, fp2, field_template, outpath, colum_num=0):
        """
        两文件合并
        """
        table_1 = xlrd.open_workbook(fp1).sheets()[0]
        table_2 = xlrd.open_workbook(fp2).sheets()[0]

        new_table = []
        table_dict = OrderedDict()
        new_table.append(field_template + table_2.row_values(0)[1:])

        for irow in range(2, table_1.nrows):   # 从Excel表中第3行开始（下标为2）
            cur_row = table_1.row_values(irow)  # 读取一行
            table_dict[cur_row[0]] = cur_row
        
        # colum_num==0 不进行平行样处理
        # colum_num!=0 进行平行样处理
        if colum_num==0:
            table_dict=self.no_parallel(table_dict,table_2,self.DIANWEI)
        else:
            table_dict=self.parallel(table_dict,table_2,0,colum_num)
            
        for row in table_dict.values():
            new_table.append(row)

        # 结果保存为Excel
        self.table_save(new_table, outpath, '采样+'+os.path.basename(fp2))


    def decrypt_merge3(self, fp1, fp2, fp3, field_template, outpath, colum1=0, colum2=0):
        """
        三文件合并
        """
        table_1 = xlrd.open_workbook(fp1).sheets()[0]
        table_2 = xlrd.open_workbook(fp2).sheets()[0]
        table_3 = xlrd.open_workbook(fp3).sheets()[0]

        new_table = []
        table_dict = OrderedDict()
        new_table.append(field_template + table_2.row_values(0)[1:] + table_3.row_values(0)[1:])

        for irow in range(2, table_1.nrows):
            cur_row = table_1.row_values(irow)
            table_dict[cur_row[0]] = cur_row

        # colum_num==0 不进行平行样处理
        # colum_num!=0 进行平行样处理
        
        table_dict=self.parallel(table_dict,table_2,0,colum1)
        if colum2!=0:
            table_dict=self.parallel(table_dict,table_3,colum1,colum2)
        else:
            table_dict=self.no_parallel(table_dict,table_3,self.DIANWEI+colum1)

        for row in table_dict.values():
            new_table.append(row)

        # 结果保存为Excel
        self.table_save(new_table, outpath, '采样+' + os.path.basename(fp2) +'+'+ os.path.basename(fp3))
    

    def decrypt_merge4(self, fp1, fp2, fp3, fp4, field_template, outpath, colum1=0, colum2=0, colum3=0):
        """
        四文件合并
        """
        table_1 = xlrd.open_workbook(fp1).sheets()[0]
        table_2 = xlrd.open_workbook(fp2).sheets()[0]
        table_3 = xlrd.open_workbook(fp3).sheets()[0]
        table_4 = xlrd.open_workbook(fp4).sheets()[0]

        new_table = []
        table_dict = OrderedDict()
        new_table.append(field_template + table_2.row_values(0)[1:] + table_3.row_values(0)[1:] + table_4.row_values(0)[1:])

        for irow in range(2, table_1.nrows):
            cur_row = table_1.row_values(irow)
            table_dict[cur_row[0]] = cur_row

        table_dict=self.parallel(table_dict,table_2,0,colum1)
        table_dict=self.parallel(table_dict,table_3,colum1,colum2)
        if colum3==0:
            table_dict=self.no_parallel(table_dict,table_4,self.DIANWEI+colum1+colum2)
        else:
            table_dict=self.parallel(table_dict,table_4,colum1+colum2,colum3)
        
        for row in table_dict.values():
            new_table.append(row)

        # 结果保存为Excel
        self.table_save(new_table, outpath, '采样+' + os.path.basename(fp2) +'+'+ os.path.basename(fp3) +'+'+ os.path.basename(fp4))


    def decrypt_merge_all(self, fp1, fp2, fp3, fp4, fp5, field_template, outpath, colum1=0, colum2=0, colum3=0):
        """
        五文件合并
        """
        table_1 = xlrd.open_workbook(fp1).sheets()[0]
        table_2 = xlrd.open_workbook(fp2).sheets()[0]
        table_3 = xlrd.open_workbook(fp3).sheets()[0]
        table_4 = xlrd.open_workbook(fp4).sheets()[0]
        table_5 = xlrd.open_workbook(fp5).sheets()[0]

        new_table = []
        table_dict = OrderedDict()
        new_table.append(field_template + table_2.row_values(0)[1:] + table_3.row_values(0)[1:] + table_4.row_values(0)[1:] + table_5.row_values(0)[1:])

        for irow in range(2, table_1.nrows):
            cur_row = table_1.row_values(irow)
            table_dict[cur_row[0]] = cur_row

        table_dict=self.parallel(table_dict,table_2,0,colum1)
        table_dict=self.parallel(table_dict,table_3,colum1,colum2)
        table_dict=self.parallel(table_dict,table_4,colum1+colum2,colum3)
        table_dict=self.no_parallel(table_dict,table_5,self.DIANWEI+colum1+colum2+colum3)

        for row in table_dict.values():
            new_table.append(row)

        # 结果保存为Excel
        self.table_save(new_table, outpath, '合并_5.xlsx')
