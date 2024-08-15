from chain import Chain

chain = Chain(difficulty=20)

i = 0
while True:
    data = input("Add something to the chain: ")
    chain.add_to_pool(data)
    chain.mine()
    if i % 5 == 0:
        print(chain.chain[i].data)
        print(chain.chain[i].hash)
        print(chain.chain[i].previous_hash)
    i += 1
