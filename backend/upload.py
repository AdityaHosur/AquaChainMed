import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load from .env

PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY")

def upload_to_pinata(filepath):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY
    }

    with open(filepath, 'rb') as file:
        files = {'file': (filepath, file)}
        response = requests.post(url, files=files, headers=headers)

    if response.status_code == 200:
        ipfs_hash = response.json()['IpfsHash']
        print(f"[INFO] Upload successful. IPFS Hash: {ipfs_hash}")  #Qman49iyuG7PZb21b3xJbuDYiqCHAVfDH1VnCqo2DDxGdr
        return ipfs_hash
    else:
        raise Exception(f"[ERROR] Upload failed: {response.text}")

ipfs_hash = upload_to_pinata("actual_watermark.png")
