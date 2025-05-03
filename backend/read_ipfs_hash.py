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

def get_ipfs_hash_from_transaction(transaction_hash: str) -> str:
    # Connect to Web3
    w3 = Web3(Web3.HTTPProvider(INFURA_URL))

    # Get transaction receipt
    tx_receipt = w3.eth.get_transaction_receipt(transaction_hash)
    logs = tx_receipt["logs"]

    # Parse logs to find the IPFS hash
    for log in logs:
        if log["address"].lower() == CONTRACT_ADDRESS.lower():
            # Decode the log data to get the IPFS hash
            log_data_hex = log["data"].hex()  # Convert HexBytes to hex string
            print(f"Log data hex: {log_data_hex}")

            # Extract the actual data
            offset = int(log_data_hex[:64], 16)  # First 32 bytes (offset)
            length = int(log_data_hex[64:128], 16)  # Next 32 bytes (length)
            print(f"Offset: {offset}, Length: {length}")

            # Extract the IPFS hash based on the offset and length
            start = 128  # Data starts after the first 64 bytes (offset + length)
            end = start + (length * 2)  # Each byte is represented by 2 hex characters
            ipfs_hash_hex = log_data_hex[start:end]
            print(f"IPFS hash hex: {ipfs_hash_hex}")

            # Decode the IPFS hash
            ipfs_hash = bytes.fromhex(ipfs_hash_hex).decode("utf-8")
            print(f"Decoded IPFS hash: {ipfs_hash}")

            return ipfs_hash.strip()  # Remove any extra spaces

    raise Exception("IPFS hash not found in transaction logs")



