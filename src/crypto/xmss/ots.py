import hashlib
from binascii import unhexlify, hexlify
import time

class WOTS:
    def __init__(self, signatures, index=0, verbose=0):
        self.signatures = signatures
        self.merkle_obj = []
        self.merkle_root = ''
        self.merkle_path = []
        self.state = 0
        self.type = 'WOTS'
        self.index = index
        self.concatpub = ""
        if verbose == 1:
            print('New W-OTS keypair generation ', str(self.index))
        self.priv, self.pub = self.random_wkey(verbose=verbose)
                
        self.concatpub = ''.join(self.pub)
        self.pubhash = hashlib.sha256(self.concatpub.encode()).hexdigest()
        return

    def random_wkey(self, w=8, verbose=0):
        priv = []
        pub = []
        start_time = time.time()
        for x in range(256 // w):
            a = self.random_key()
            priv.append(a)
            for y in range(2 ** w - 1):
                a = hashlib.sha256(a.encode()).hexdigest()
            pub.append(hashlib.sha256(a.encode()).hexdigest())

        elapsed_time = time.time() - start_time
        if verbose == 1:
            print(elapsed_time)
        return priv, pub

    def random_key(self, n=32):
        from os import urandom
        return hexlify(urandom(n)).decode()

    def screen_print(self):
        print(self.priv)
        print(self.pub)
        print(self.concatpub)
        print(self.pubhash)
        return