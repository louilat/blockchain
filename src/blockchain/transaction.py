import hashlib
from ecdsa import SigningKey, VerifyingKey, BadSignatureError


class Transaction:
    def __init__(self, sender: str, receiver: str, amount: float) -> None:
        self.sender: str = sender
        self.receiver: str = receiver
        self.amount: float = amount
        self.message: str = f"{sender}{receiver}{amount}"
        h = hashlib.sha256()
        h.update(self.message.encode("utf-8"))
        self.hash: str = h.hexdigest()
        self.signature: bytes = b""

    def sign(self, private_key: SigningKey) -> None:
        signature = private_key.sign(self.hash.encode("utf-8"))
        self.signature = signature

    def verify(self, public_key: VerifyingKey) -> bool:
        try:
            unforgeable = public_key.verify(
                self.signature,
                self.hash.encode("utf-8"),
            )
            authentic = public_key.to_string().hex() == self.sender
            return unforgeable and authentic
        except BadSignatureError:
            return False

    def __str__(self):
        return f"SENDER:: {self.sender} --- RECEIVER:: {self.receiver} --- AMOUNT:: {self.amount}"
