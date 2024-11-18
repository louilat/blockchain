from src.blockchain.chain import Chain
from ecdsa import SigningKey
from src.blockchain.transaction import Transaction

private_key1 = SigningKey.generate()
public_key1 = private_key1.verifying_key

private_key2 = SigningKey.generate()
public_key2 = private_key2.verifying_key

chain = Chain(msg_sender=public_key1.to_string().hex())

transac1 = Transaction(
    sender_public_key=public_key1,
    receiver=public_key2.to_string().hex(),
    amount=12.2,
)
transac1.sign(private_key1)

chain.add_to_pool(transac1)

chain.mine()
