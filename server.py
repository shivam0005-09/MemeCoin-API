from flask import Flask, request, jsonify
from myblockchain import Blockchain, Wallet  # Import MemeCoin Blockchain

app = Flask(__name__)

# Create Blockchain Instance
meme_coin = Blockchain()

# Create a miner wallet (For testing)
miner_wallet = Wallet()

@app.route('/wallet/new', methods=['GET'])
def new_wallet():
    """Create a new wallet"""
    wallet = Wallet()
    return jsonify({
        "address": wallet.address,
        "private_key": wallet.get_private_key()
    })

@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    """Check balance of a wallet"""
    balance = meme_coin.get_balance(address)
    return jsonify({"address": address, "balance": balance})

@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    """Create a new transaction"""
    data = request.json
    sender = data['from']
    recipient = data['to']
    amount = data['amount']
    
    if not sender or not recipient or not amount:
        return jsonify({"error": "Missing transaction data"}), 400
    
    meme_coin.create_transaction(sender, recipient, amount)
    return jsonify({"message": "Transaction added"}), 201

@app.route('/mine', methods=['GET'])
def mine():
    """Mine pending transactions and reward the miner"""
    meme_coin.mine_pending_transactions(miner_wallet.address)
    return jsonify({"message": "Block mined!", "miner_balance": meme_coin.get_balance(miner_wallet.address)})

@app.route('/chain', methods=['GET'])
def get_chain():
    """Return the full blockchain"""
    chain_data = []
    for block in meme_coin.chain:
        chain_data.append({
            "index": block.index,
            "hash": block.hash,
            "previous_hash": block.previous_hash,
            "transactions": block.transactions
        })
    return jsonify({"chain": chain_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
