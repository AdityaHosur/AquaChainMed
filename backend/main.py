from fastapi import FastAPI, File, UploadFile, Form, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from watermark import generate_actual_watermark, embed_watermark_lsb
from upload import upload_to_pinata
from store_ipfs_hash import store_ipfs_hash_on_blockchain
import cv2
import numpy as np
import os
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
            # Echo the message back to the client (for testing)
            await websocket.send_text(f"Message received: {data}")
    except Exception as e:
        print(f"WebSocket connection closed: {e}")


@app.post("/api/watermark")
async def watermark_images(
    medical_image: UploadFile = File(...), watermark_image: UploadFile = File(...)):
    # Save uploaded files temporarily
    medical_image_path = f"temp_{medical_image.filename}"
    watermark_image_path = f"temp_{watermark_image.filename}"

    with open(medical_image_path, "wb") as f:
        f.write(await medical_image.read())

    with open(watermark_image_path, "wb") as f:
        f.write(await watermark_image.read())

    # Read the images
    host_image = cv2.imread(medical_image_path)
    host_shape = host_image.shape[:2]

    # Generate the actual watermark
    actual_watermark, _ = generate_actual_watermark(watermark_image_path, host_shape)

    # Save the actual watermark as an image
    actual_watermark_path = "actual_watermark.png"
    cv2.imwrite(actual_watermark_path, actual_watermark * 255)

    # Embed the watermark
    watermarked_image = embed_watermark_lsb(medical_image_path, actual_watermark)

    # Save the watermarked image
    watermarked_image_path = "watermarked_image.png"
    cv2.imwrite(watermarked_image_path, watermarked_image)

    # Convert the watermarked image to base64
    with open(watermarked_image_path, "rb") as img_file:
        watermarked_image_base64 = base64.b64encode(img_file.read()).decode("utf-8")

    # Upload the actual watermark to IPFS
    watermark_ipfs_hash = upload_to_pinata(actual_watermark_path)

    # Store the IPFS hash in the blockchain
    blockchain_tx_hash = store_ipfs_hash_on_blockchain(watermark_ipfs_hash)

    # Clean up temporary files
    os.remove(medical_image_path)
    os.remove(watermark_image_path)
    os.remove(watermarked_image_path)
    os.remove(actual_watermark_path)

    return {
        "message": "Watermarking successful",
        "watermarked_image": watermarked_image_base64,
        "watermark_ipfs_hash": watermark_ipfs_hash,
        "blockchain_tx_hash": blockchain_tx_hash,
    }

@app.post("/api/verify")
async def verify_watermark(watermarked_image: UploadFile = File(...),transaction_hash: str = Form(...)):
    if not transaction_hash:
        return {"error": "Transaction hash is required"}

    # Save the uploaded watermarked image temporarily
    watermarked_image_path = f"temp_{watermarked_image.filename}"
    with open(watermarked_image_path, "wb") as f:
        f.write(await watermarked_image.read())

    try:
        # Retrieve IPFS hash from the blockchain
        from read_ipfs_hash import get_ipfs_hash_from_transaction
        ipfs_hash = get_ipfs_hash_from_transaction(transaction_hash)

        # Download the watermark from IPFS
        from download import download_from_ipfs
        downloaded_watermark_path = "downloaded_actual_watermark.png"
        download_from_ipfs(ipfs_hash)

        # Extract the watermark from the uploaded watermarked image
        from extract import extract_lsb_watermark
        extracted_watermark_path = "extracted_watermark.png"
        extract_lsb_watermark(watermarked_image_path)

        # Perform XOR verification
        from verify import verify_watermark
        verification_result = verify_watermark(
            downloaded_path=downloaded_watermark_path,
            extracted_path=extracted_watermark_path
        )

        # Clean up temporary files
        os.remove(watermarked_image_path)
        os.remove(downloaded_watermark_path)
        os.remove(extracted_watermark_path)

        return {"message": verification_result}

    except Exception as e:
        # Clean up temporary files in case of an error
        if os.path.exists(watermarked_image_path):
            os.remove(watermarked_image_path)
        if os.path.exists("downloaded_actual_watermark.png"):
            os.remove("downloaded_actual_watermark.png")
        if os.path.exists("extracted_watermark.png"):
            os.remove("extracted_watermark.png")

        return {"error": str(e)}