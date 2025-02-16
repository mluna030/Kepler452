from crypto.xmss import XMSS
from crypto.ots import WOTS
from crypto.merkle import Merkle
import sys

message = "Hello"

if len(sys.argv) > 1:
    message = sys.argv[1]

print("Message:\t", message)
d = XMSS(4)  # create XMSS instance with 4 signatures

print("Public key [0][0]:", d.pubs[0][0])
print("Private key [0][0]:", d.privs[0][0])

print("Merkle root:", d.root)

sig = d.SIGN(message)
print("Signature [0]:", sig[1][0])

print("Verified MSS:\t", d.VERIFY(message, sig))

print("Merkle path:\t", d.merkle_path)

print("Verify root\t", d.verify_auth(sig[2], sig[3], sig[4], d.PK))