import hashlib
import os
from Crypto.Cipher import AES
import base64

class Encrypt():
    '''encrypts sensitive data for querying with database'''
    def __init__(self, password):
        self.key = __keyFromPassword(self,password)

    def __pad(s): 
        return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size) 

    def __unpad(data):
        return data[0:-ord(data[-1])]
    
    def __cipher(key='0'*32, iv='0'*16):
        return AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
    
    def encrypt_token(key,data):
        return __cipher(key["cipherKey"]).encrypt(__pad(data)).hex()
    

    def decrypt_token(key,hex_data):
        data = bytes.fromhex(hex_data)
        return unpad(_cipher(key["cipherKey"]).decrypt(data).decode())
    

    def bloatString(string, salt):
        return hashlib.pbkdf2_hmac('sha512', string.encode('utf8') , salt , 100000).hex()
    

    def __keyFromPassword(self,password):
        bloated_string = bloatString(password, base64.b64encode(os.urandom(16)))
        return {"cipherKey": bloated_string[:24]," hashingSalt": bloated_string[24:]}