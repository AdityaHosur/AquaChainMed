import os
from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv

load_dotenv()
install_solc('0.8.0')

# Load environment
INFURA_URL = os.getenv("INFURA_URL")
ACCOUNT = os.getenv("ACCOUNT")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Connect to Ethereum
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Load Solidity source
with open("contract.sol", "r") as file:
    source_code = file.read()

# Compile the contract
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        "contract.sol": {
            "content": source_code
        }
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
            }
        }
    }
}, solc_version="0.8.0")

# Extract ABI and bytecode
abi = compiled_sol['contracts']['contract.sol']['MedicalImageHashStore']['abi']
bytecode = compiled_sol['contracts']['contract.sol']['MedicalImageHashStore']['evm']['bytecode']['object']

# Deploy the contract
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(ACCOUNT)

transaction = contract.constructor().build_transaction({
    'from': ACCOUNT,
    'nonce': nonce,
    'gas': 3000000,
    'gasPrice': w3.to_wei('10', 'gwei')
})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
print("Deploying contract...")

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract deployed at:", tx_receipt.contractAddress)

# Save ABI to a file (for later use)
with open("contract_abi.json", "w") as f:
    import json
    json.dump(abi, f)
