from key_repo import KeyRepo

kr = KeyRepo('./keys_vigenere')
kr.clear()
kr.gen_vigenere()