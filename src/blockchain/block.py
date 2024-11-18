import hashlib
from datetime import datetime
from src.blockchain.transaction import Transaction
from pymerkle import InmemoryTree as MerkleTree


class BlockHeader:
    def __init__(self, hashPrevBlock: str, hashMerkleRoot: str):
        self.version: int = 0
        self.hashPrevBlock: str = hashPrevBlock
        self.hashMerkleRoot: str = hashMerkleRoot
        self.time: datetime = datetime.now()
        self.bits: int = 20
        self.nonce: int = 0

    def increment(self):
        self.nonce += 1

    def __str__(self):
        return f"{self.version}{self.hashPrevBlock}{self.hashMerkleRoot}{self.time}{self.bits}{self.nonce}"


class Block:
    def __init__(self, hashPrevBlock: str, transactions: list[Transaction]):
        self.constant: int = 0
        self.blockSize: int = 0
        self.transactions: list[Transaction] = transactions
        self.transactionsNumber: int = len(transactions)
        hashMerkleRoot = self._compute_merkle_root().hex()
        self.header: BlockHeader = BlockHeader(hashPrevBlock, hashMerkleRoot)
        self.hashBlock: str = str()

    def _compute_merkle_root(self) -> str:
        tree = MerkleTree(algorithm="sha256")
        for transaction in self.transactions:
            tree.append_entry(str(transaction).encode("utf-8"))
        return tree.get_state()

    def __str__(self):
        return str(self.header)

    def mine(self):
        h = hashlib.sha256()
        h.update(str(self).encode("utf-8"))
        value = h.hexdigest()
        while int(value, 16) > 2 ** (256 - self.header.bits):
            self.header.increment()
            h = hashlib.sha256()
            h.update(str(self).encode("utf-8"))
            value = h.hexdigest()
        self.hashBlock = value
        print(f"The block as been successfully mined with nonce {self.header.nonce}")

    # def __str__(self):
    #     return f"{self.previous_hash}{self.data}{self.nonce}"

    # def mine(self):
    #     h = hashlib.sha256()
    #     h.update(str(self).encode("utf-8"))
    #     value = h.hexdigest()
    #     while int(value, 16) > 2 ** (256 - self.difficulty):
    #         self.nonce += 1
    #         h = hashlib.sha256()
    #         h.update(str(self).encode("utf-8"))
    #         value = h.hexdigest()
    #     self.hash = value
