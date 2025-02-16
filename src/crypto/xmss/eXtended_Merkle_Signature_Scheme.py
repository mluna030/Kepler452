from .hmac_drbg import HMAC_DRBG
from .merkle import Merkle
from .ots import WOTS
import hashlib
from binascii import hexlify, unhexlify
import time

class XMSS:
    def __init__(self, signatures, SEED=None):
        self.type = 'XMSS'
        self.index = 0
        if signatures > 4986:
            signatures = 4986
        self.signatures = signatures
        self.remaining = signatures
        
        self.SEED, self.public_SEED, self.private_SEED = self.new_keys(SEED)
        self.hexpublic_SEED = hexlify(self.public_SEED).decode()
        self.hexprivate_SEED = hexlify(self.private_SEED).decode()
        self.hexSEED = hexlify(self.SEED).decode()
        self.mnemonic = self.seed_to_mnemonic(self.SEED)

        self.tree, self.x_bms, self.l_bms, self.privs, self.pubs = self.xmss_tree(n=signatures, private_SEED=self.private_SEED, public_SEED=self.public_SEED)
        self.root = ''.join(self.tree[-1])

        self.PK = [self.root, self.x_bms, self.l_bms]
        self.catPK = [''.join(self.root), ''.join(self.x_bms), ''.join(self.l_bms)]
        self.address_long = 'Q' + hashlib.sha256(''.join(self.catPK).encode()).hexdigest() + hashlib.sha256(hashlib.sha256(''.join(self.catPK).encode()).hexdigest().encode()).hexdigest()[:4]

        self.PK_short = [self.root, self.hexpublic_SEED]
        self.catPK_short = self.root + self.hexpublic_SEED
        self.address = 'Q' + hashlib.sha256(self.catPK_short.encode()).hexdigest() + hashlib.sha256(hashlib.sha256(self.catPK_short.encode()).hexdigest().encode()).hexdigest()[:4]

        self.addresses = [(0, self.address, self.signatures)]
        self.subtrees = [(0, self.signatures, self.tree, self.x_bms, self.PK_short)]

    def new_keys(self, seed=None, n=9999):
        if not seed:
            seed = self.SEED(48)
        private_SEED = self.GEN(seed, 1, l=48)
        public_SEED = self.GEN(seed, n, l=48)
        return seed, public_SEED, private_SEED

    def GEN(self, SEED, i, l=32):
        z = HMAC_DRBG(SEED)
        for x in range(i):
            y = z.generate(l)
        return y

    def seed_to_mnemonic(self, SEED):
        if len(SEED) != 48:
            print('ERROR: SEED is not 48 bytes in length..')
            return False
        words = []
        y = 0
        for x in range(16):
            three_bytes = format(ord(SEED[y]), '08b') + format(ord(SEED[y + 1]), '08b') + format(ord(SEED[y + 2]), '08b')
            words.append(wordlist[int(three_bytes[:12], 2)])
            words.append(wordlist[int(three_bytes[12:], 2)])
            y += 3
        return ' '.join(words)

    def xmss_tree(self, n, private_SEED, public_SEED):
        h = ceil(log(n, 2))
        leafs = []
        pubs = []
        privs = []

        rand_keys = self.GEN_range(public_SEED, 1, 14 + 2 * n + int(h), 32)
        l_bms = rand_keys[:14]
        x_bms = rand_keys[14:]
        
        sk_keys = self.GEN_range(private_SEED, 1, n, 32)

        for x in range(n):
            priv, pub = self.random_wpkey_xmss(seed=sk_keys[x])
            leaf = self.l_tree(pub, l_bms)
            leafs.append(leaf)
            pubs.append(pub)
            privs.append(priv)
        
        xmss_array = []
        xmss_array.append(leafs)
        
        p = 0
        for x in range(int(h)):
            next_layer = []
            i = len(xmss_array[x]) % 2 + len(xmss_array[x]) / 2
            z = 0
            for y in range(i):
                if len(xmss_array[x]) == z + 1:
                    next_layer.append(xmss_array[x][z])
                    p += 1
                else:
                    next_layer.append(hashlib.sha256(hex(int(xmss_array[x][z], 16) ^ int(x_bms[p], 16))[2:-1] + hex(int(xmss_array[x][z + 1], 16) ^ int(x_bms[p + 1], 16))[2:-1].encode()).hexdigest())
                    p += 2
                z += 2 
            xmss_array.append(next_layer)

        return xmss_array, x_bms, l_bms, privs, pubs