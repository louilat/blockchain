from block import Block
import hashlib


class Chain:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        initial_block = Block("Initial_Block", "previous_hash")
        initial_block.mine()
        self.chain = [initial_block]
        self.pool = []

    def proof_of_work(self, block: Block):
        h = hashlib.sha256()
        h.update(str(block).encode("utf-8"))
        return (
            block.hash == h.hexdigest()
            and int(block.hash, 16) < 2 ** (256 - self.difficulty)
            and block.previous_hash == self.chain[-1].hash
        )

    def add_to_chain(self, block):
        if self.proof_of_work(block):
            self.chain.append(block)

    def add_to_pool(self, data: str):
        self.pool.append(data)

    def mine(self):
        if len(self.pool) > 0:
            data = " | ".join(self.pool)
            block = Block(
                data, previous_hash=self.chain[-1].hash, difficulty=self.difficulty
            )
            block.mine()
            self.add_to_chain(block)
            self.pool = []
            print("The data has successfully been added to the chain.")
        else:
            print("Nothing to mine.")
