import requests

def download_from_ipfs(ipfs_hash):
    # Ensure the IPFS hash is valid
    url = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
    print(f"Downloading from IPFS URL: {url}")

    try:
        response = requests.get(url, timeout=10)  # Add a timeout to avoid hanging
        response.raise_for_status()  # Raise an exception for HTTP errors

        if response.status_code == 200:
            with open("downloaded_actual_watermark.png", "wb") as f:
                f.write(response.content)
            print("Downloaded watermark from IPFS successfully!")
        else:
            raise Exception(f"Failed to download from IPFS: {response.status_code}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error downloading from IPFS: {e}")


