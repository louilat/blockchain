from block import Block

b = Block("Coucou", difficulty=20)
b.mine()
print("hash = ", b.hash)
print("nonce = ", b.nonce)
print("condition = ", int(b.hash, 16) < 2**(256-20))
