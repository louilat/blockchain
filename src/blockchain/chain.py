from src.blockchain.block import Block
from src.blockchain.transaction import Transaction
from ecdsa import SigningKey
import hashlib


class Chain:
    def __init__(self, msg_sender: str, mine_amount: int = 1e6) -> None:
        virtual_private_key = SigningKey.generate()
        virtual_public_key = virtual_private_key.verifying_key
        initial_transaction = Transaction(
            sender_public_key=virtual_public_key,
            receiver=msg_sender,
            amount=mine_amount,
        )
        initial_transaction.sign(virtual_private_key)
        initial_block = Block("Genesis", [initial_transaction])
        initial_block.mine()
        self.chain: list[Block] = [initial_block]
        self.pool: list[Transaction] = []

    def proof_of_work(self, block: Block) -> bool:
        # Target
        h = hashlib.sha256()
        h.update(str(block).encode("utf-8"))
        value = h.hexdigest()
        if int(value, 16) >= 2 ** (256 - block.header.bits):
            print("Target not valid")
            return False

        # hashMerkleRoot
        if block._compute_merkle_root().hex() != block.header.hashMerkleRoot:
            print("hashMarkleRoot not valid")
            return False

        # hashPrevBlock
        if block.header.hashPrevBlock != self.chain[-1].hashBlock:
            print("hashPrevBlock not valid")
            return False

        # Check valid transactions
        for i, transaction in enumerate(block.transactions):
            if not self._isTransactionValid(transaction):
                print(f"Transaction {i} is not valid: amount does not exist")
                return False
            if not transaction.verify():
                print(f"Transaction {i} is not valid: invalid signature")
                return False
        print("The block has been successfully verified.")
        return True

    def _isTransactionValid(self, transaction: Transaction) -> bool:
        available_amount = 0
        amount = transaction.amount
        block_number = 1
        sender = transaction.sender
        while available_amount < amount and block_number <= len(self.chain):
            current_block = self.chain[-block_number]
            for transac in reversed(current_block.transactions):
                if transac.receiver == sender:
                    available_amount += transac.amount
                elif transac.sender == sender:
                    available_amount -= transac.amount

                if available_amount >= amount:
                    return True
            block_number += 1
        return False

    def add_to_chain(self, block):
        if self.proof_of_work(block):
            self.chain.append(block)
        else:
            raise Exception("Proof of work invalid")

    def add_to_pool(self, data: str):
        self.pool.append(data)

    def mine(self):
        if len(self.pool) > 0:
            new_block = Block(
                hashPrevBlock=self.chain[-1].hashBlock,
                transactions=self.pool,
            )
            new_block.mine()
            try:
                self.add_to_chain(new_block)
                self.pool = []
                print("The data has successfully been added to the chain.")
            except Exception:
                print("Invalid proof of work, transactions not added to the chain.")
        else:
            print("Nothing to mine.")
