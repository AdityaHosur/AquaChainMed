import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
INFURA_URL = os.getenv("INFURA_URL")
ACCOUNT = os.getenv("ACCOUNT")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = "0xDF743e0D6b98A1E8265a219b382d8e00263e90D3"  # Replace with your deployed address

# Connect to Web3
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Load ABI
with open("contract_abi.json", "r") as file:
    contract_abi = json.load(file)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

# IPFS hash to store
ipfs_hash = "Qman49iyuG7PZb21b3xJbuDYiqCHAVfDH1VnCqo2DDxGdr"  # Replace this with your real IPFS hash

# Prepare transaction
nonce = w3.eth.get_transaction_count(ACCOUNT)
txn = contract.functions.storeHash(ipfs_hash).build_transaction({
    "chainId": w3.eth.chain_id,
    "gas": 200000,
    "gasPrice": w3.eth.gas_price,
    "nonce": nonce
})

# Sign and send transaction
signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

print("Transaction sent. Hash:", tx_hash.hex())

# Optional: Wait for confirmation
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Transaction confirmed in block:", tx_receipt.blockNumber)
