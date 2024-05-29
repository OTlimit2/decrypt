
# ciphertext="150421-3Q79M020323"

# print(ciphertext[:7])
# print(ciphertext[-2:])
# print(ciphertext[-4:-2])
# print(ciphertext[7:-4])

def is_number(s):
        '''
        判断是否为数字
        '''
        try:
            float(s)
            return True
        except ValueError:
            pass
 
        return False

a="12.3"
b=""
c="/"

print(is_number(a))
print(is_number(b))
print(is_number(c))