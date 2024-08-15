import hashlib


class Block:
    def __init__(self, data: str, difficulty: int = 10):
        self.hash = None
        self.nonce = 0
        self.data = data
        self.difficulty = difficulty

    def __str__(self):
        return f"{self.data}{self.nonce}"

    def mine(self):
        h = hashlib.sha256()
        h.update(str(self).encode('utf-8'))
        value = h.hexdigest()
        while int(value, 16) > 2**(256 - self.difficulty):
            self.nonce += 1
            h = hashlib.sha256()
            h.update(str(self).encode('utf-8'))
            value = h.hexdigest()
        self.hash = value
