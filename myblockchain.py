import hashlib
import time
import json
import random
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

class Wallet:
    def __init__(self):
        # Generate Private Key
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()

        # Create Wallet Address
        self.address = self.generate_address()

    def generate_address(self):
        # Create a hash-based wallet address from the public key
        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return hashlib.sha256(public_pem).hexdigest()[:32]  # First 32 characters of the hash

    def get_private_key(self):
        # Export Private Key as PEM format (for backup)
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{json.dumps(self.transactions)}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"🎉 Block Mined! Hash: {self.hash}")

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.mining_reward = 10
        self.balances = {}

    def create_genesis_block(self):
        return Block(0, "0", time.time(), ["Genesis Block"])

    def mine_pending_transactions(self, miner_address):
        if not self.pending_transactions:
            print("⛏️ No transactions to mine!")
            return

        new_block = Block(len(self.chain), self.chain[-1].hash, time.time(), self.pending_transactions)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

        # Reward the miner
        self.balances[miner_address] = self.balances.get(miner_address, 0) + self.mining_reward
        print(f"🎁 Miner {miner_address} received {self.mining_reward} MemeCoins!")

        self.pending_transactions = []

    def create_transaction(self, sender, recipient, amount):
        if self.balances.get(sender, 0) < amount:
            print("❌ Insufficient balance!")
            return

        self.pending_transactions.append({"from": sender, "to": recipient, "amount": amount})
        self.balances[sender] -= amount
        self.balances[recipient] = self.balances.get(recipient, 0) + amount
        print(f"💸 Transaction Added: {sender} → {recipient} ({amount} MemeCoins)")

    def get_balance(self, address):
        return self.balances.get(address, 0)

    def print_chain(self):
        for block in self.chain:
            print(f"\n📦 Block {block.index}:")
            print(f"   Hash: {block.hash}")
            print(f"   Previous Hash: {block.previous_hash}")
            print(f"   Transactions: {block.transactions}")

# 🚀 Welcome Message
print("\n🚀 Welcome to MemeCoin Blockchain! 🚀\n")

# 🔑 Create Wallets for Users
wallet_A = Wallet()
wallet_B = Wallet()
miner_wallet = Wallet()

print(f"💳 Alice's Wallet Address: {wallet_A.address}")
print(f"🔑 Alice's Private Key (Keep Secret!):\n{wallet_A.get_private_key()}\n")

print(f"💳 Bob's Wallet Address: {wallet_B.address}")
print(f"🔑 Bob's Private Key (Keep Secret!):\n{wallet_B.get_private_key()}\n")

# 🏦 Create Blockchain
meme_coin = Blockchain()

# 🎁 Give Starting Balance
meme_coin.balances[wallet_A.address] = 50
meme_coin.balances[wallet_B.address] = 20

# 🏦 Transactions
meme_coin.create_transaction(wallet_A.address, wallet_B.address, 5)
meme_coin.create_transaction(wallet_B.address, wallet_A.address, 2)

# ⛏️ Mining (Miner gets rewards)
meme_coin.mine_pending_transactions(miner_wallet.address)

# 💰 Check Balances
print(f"\n💰 Alice's Balance: {meme_coin.get_balance(wallet_A.address)} MemeCoins")
print(f"💰 Bob's Balance: {meme_coin.get_balance(wallet_B.address)} MemeCoins")
print(f"💰 Miner's Balance: {meme_coin.get_balance(miner_wallet.address)} MemeCoins")

# 📜 Print Blockchain
meme_coin.print_chain()
