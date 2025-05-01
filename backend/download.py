import requests

def download_from_ipfs(ipfs_hash):
    url = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
    response = requests.get(url)
    
    if response.status_code == 200:
        with open("downloaded_actual_watermark.png", "wb") as f:
            f.write(response.content)
        print("Downloaded watermark from IPFS successfully!")
    else:
        raise Exception(f"Failed to download from IPFS: {response.status_code}")

# Example usage:
ipfs_hash = "Qman49iyuG7PZb21b3xJbuDYiqCHAVfDH1VnCqo2DDxGdr"  # retrieved from smart contract
download_from_ipfs(ipfs_hash)
