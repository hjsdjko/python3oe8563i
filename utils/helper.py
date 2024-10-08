#coding:utf-8
import hashlib
import decimal
from Crypto.Cipher import DES,AES
from Crypto.Util.Padding import pad,unpad
import base64

def computeMD5(message):
    m = hashlib.md5()
    m.update(message.encode(encoding='utf-8'))
    return m.hexdigest()


def decimalEncoder(o):
    if isinstance(o, decimal.Decimal):
        return float(o)
    return o

def BytesEncoder(o):
    if isinstance(o, bytes):
        return str(o, encoding='utf-8')
    return o

if __name__=='__main__':
    result = computeMD5('123456')
    print(result)