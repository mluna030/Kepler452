import hashlib
from binascii import hexlify, unhexlify
from os import urandom

def sha256(message):
    return hashlib.sha256(str(message).encode('utf-8')).hexdigest()

def random_key(n=32):
    return hexlify(urandom(n)).decode()

def SEED(n=48):
    return urandom(n)