import datetime
import hashlib

# Class represents a single block in the blockchain.
class Block:
    def __init__(self, data, blockNo=0, previous_hash=0x0):
        self.data = data                      # Data stored in the block.
        self.blockNo = blockNo                # Block number in the chain.
        self.previous_hash = previous_hash    # Hash of the previous block.
        self.next = None                      # Pointer to the next block.
        self.nonce = 0                        # Number used to vary hash output during mining.
        self.timestamp = datetime.datetime.now()

    def calculate_hash(self):
        h = hashlib.sha256()
        h.update(
            str(self.nonce).encode('utf-8') +
            str(self.data).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.blockNo).encode('utf-8')
        )
        return h.hexdigest()

    def __str__(self):
        return (f"Block Hash: {self.calculate_hash()}\n"
                f"BlockNo: {self.blockNo}\n"
                f"Block Data: {self.data}\n"
                f"Nonce: {self.nonce}\n"
                f"--------------")

# Class that manages the entire blockchain
class Blockchain:

    MAX_NONCE = 2**32      # Maximum attempts to find a valid nonce during mining.
    
    def __init__(self, difficulty=20, genesis_data="Genesis"):
        self.diff = difficulty              # Difficulty level of mining
        self.target = 2 ** (256-self.diff)  # Target threshold for a valid hash

        self.genesis_block = Block(genesis_data)
        self.head = self.genesis_block 
        self.current_block = self.genesis_block

    # Adds a mined block to the blockchain
    def add(self, block):
        block.previous_hash = self.current_block.calculate_hash()
        block.blockNo = self.current_block.blockNo + 1

        self.current_block.next = block      # Link current block to the new block.
        self.current_block = block           # Update current block pointer.

    # Mining process.
    def mine(self, block):
        for n in range(self.MAX_NONCE):
            if int(block.calculate_hash(), 16) <= self.target:
                self.add(block)
                print(f"Block #{block.blockNo} successfully mined!")
                print(block)
                return True
            else:
                block.nonce += 1
        
        print(f"Failed to mine block after {self.MAX_NONCE} attempts.")
        return False

# Create the blockchain and mine blocks.
blockchain = Blockchain()

# Mine and add 10 blocks to the chain.
for n in range(10):
    blockchain.mine(Block("Block " + str(n+1)))

while blockchain.head != None:
    print(blockchain.head)
    blockchain.head = blockchain.head.next