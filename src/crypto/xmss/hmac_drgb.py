import hmac
import hashlib

class HMAC_DRBG:
    def __init__(self, entropy, personalisation_string="", security_strength=256):
        self.security_strength = security_strength
        self.instantiate(entropy, personalisation_string)

    def hmac(self, key, data):
        return hmac.new(key, data, hashlib.sha256).digest()

    def generate(self, num_bytes, requested_security_strength=256):
        if (num_bytes * 8) > 7500:
            raise RuntimeError("generate cannot generate more than 7500 bits in a single call.")

        if requested_security_strength > self.security_strength:
            raise RuntimeError("requested_security_strength exceeds this instance's security_strength (%d)" % self.security_strength)

        if self.reseed_counter >= 10000:
            return None

        temp = b""

        while len(temp) < num_bytes:
            self.V = self.hmac(self.K, self.V)
            temp += self.V

        self.update(None)
        self.reseed_counter += 1

        return temp[:num_bytes]

    def reseed(self, entropy):
        self.update(entropy)
        self.reseed_counter = 1
        return

    def instantiate(self, entropy, personalisation_string=""):
        seed_material = entropy + personalisation_string
        
        self.K = b"\x00" * 32
        self.V = b"\x01" * 32

        self.update(seed_material)
        self.reseed_counter = 1
        return

    def update(self, seed_material=None):
        self.K = self.hmac(self.K, self.V + b"\x00" + (b"" if seed_material is None else seed_material))
        self.V = self.hmac(self.K, self.V)

        if seed_material is not None:
            self.K = self.hmac(self.K, self.V + b"\x01" + seed_material)
            self.V = self.hmac(self.K, self.V)

        return