from flask import Flask, jsonify, request
import hashlib
import time

app = Flask(__name__)

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Create the first block (genesis block)
        genesis_block = Block(0, "0", time.time(), "Genesis Block", self.calculate_hash(0))
        self.chain.append(genesis_block)

    def create_block(self, data):
        # Create a new block with transaction data
        previous_block = self.chain[-1]
        new_index = previous_block.index + 1
        new_timestamp = time.time()
        new_hash = self.calculate_hash(new_index)
        new_block = Block(new_index, previous_block.hash, new_timestamp, data, new_hash)
        self.chain.append(new_block)

    def calculate_hash(self, index):
        # Calculate the hash for a given block
        return hashlib.sha256(str(index).encode()).hexdigest()

    def to_dict(self):
        # Convert the blockchain to a dictionary
        return [vars(block) for block in self.chain]

# Create a blockchain
shop_blockchain = Blockchain()

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    # Retrieve the entire blockchain
    return jsonify(shop_blockchain.to_dict()), 200

@app.route('/blockchain/add', methods=['POST'])
def add_block():
    # Add a new block to the blockchain
    data = request.get_json()
    shop_blockchain.create_block(data)
    return jsonify({"message": "Block added to the blockchain"}), 201

if __name__ == '__main__':
    app.run()
