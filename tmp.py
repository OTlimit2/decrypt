from base64 import b64encode, b64decode

def bytes_xor(s1, s2):
    """按位异或s1 s2"""
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))


if __name__ == '__main__':
    plaintext = '123456-XY-102'
    key = '123456'

    prefix = plaintext[:7]
    letter = plaintext[7:9]
    number = plaintext[10:]

    letter_bytes = bytes(letter, encoding='ascii')
    letter_int = int.from_bytes(letter_bytes, byteorder='big')
    ciphertext = letter_int << 10
    ciphertext |= int(number)
    ciphertext = ciphertext.to_bytes(4, byteorder='big')
    ciphertext = b64encode(ciphertext)
