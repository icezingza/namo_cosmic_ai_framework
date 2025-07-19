# security_systems/quantum_encryption.py

import hashlib

class QuantumEncryption:
    def encrypt(self, data):
        """
        เข้ารหัสข้อมูลด้วย SHA3-512
        """
        encoded = str(data).encode()
        return hashlib.sha3_512(encoded).hexdigest()

    def verify_integrity(self, original, encrypted):
        return self.encrypt(original) == encrypted
