import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# Load env variables
INFURA_URL = os.getenv("INFURA_URL")
CONTRACT_ADDRESS = "0xDF743e0D6b98A1E8265a219b382d8e00263e90D3"  # Replace this
ACCOUNT = os.getenv("ACCOUNT")

# Connect to Web3
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Load contract ABI
with open("contract_abi.json", "r") as f:
    contract_abi = json.load(f)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

# Call getHash() function
ipfs_hash = contract.functions.getHash(ACCOUNT).call()
print("Retrieved IPFS hash from blockchain:", ipfs_hash)

