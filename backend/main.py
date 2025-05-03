from fastapi import FastAPI, File, UploadFile, Form, WebSocket, WebSocketDisconnect
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

class WebSocketManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

websocket_manager = WebSocketManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
        print("WebSocket connection closed")


@app.post("/api/watermark")
async def watermark_images(
    medical_image: UploadFile = File(...),
    watermark_image: UploadFile = File(...),
):
    try:
        # Save uploaded files temporarily
        medical_image_path = f"temp_{medical_image.filename}"
        watermark_image_path = f"temp_{watermark_image.filename}"

        # Send progress update via WebSocket
        await websocket_manager.broadcast("Saving uploaded files...")
        with open(medical_image_path, "wb") as f:
            f.write(await medical_image.read())
        with open(watermark_image_path, "wb") as f:
            f.write(await watermark_image.read())

        # Read the images
        await websocket_manager.broadcast("Reading medical image...")
        host_image = cv2.imread(medical_image_path)
        host_shape = host_image.shape[:2]

        # Generate the actual watermark
        await websocket_manager.broadcast("Generating watermark...")
        actual_watermark, _ = generate_actual_watermark(watermark_image_path, host_shape)

        # Save the actual watermark as an image
        actual_watermark_path = "actual_watermark.png"
        cv2.imwrite(actual_watermark_path, actual_watermark * 255)

        # Embed the watermark
        await websocket_manager.broadcast("Embedding watermark into medical image...")
        watermarked_image = embed_watermark_lsb(medical_image_path, actual_watermark)

        # Save the watermarked image
        watermarked_image_path = "watermarked_image.png"
        cv2.imwrite(watermarked_image_path, watermarked_image)

        # Convert the watermarked image to base64
        await websocket_manager.broadcast("Converting watermarked image to base64...")
        with open(watermarked_image_path, "rb") as img_file:
            watermarked_image_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        # Upload the actual watermark to IPFS
        await websocket_manager.broadcast("Uploading watermark to IPFS...")
        watermark_ipfs_hash = upload_to_pinata(actual_watermark_path)

        # Store the IPFS hash in the blockchain
        await websocket_manager.broadcast("Storing IPFS hash on blockchain...")
        blockchain_tx_hash = store_ipfs_hash_on_blockchain(watermark_ipfs_hash)

        # Clean up temporary files
        os.remove(medical_image_path)
        os.remove(watermark_image_path)
        os.remove(watermarked_image_path)
        os.remove(actual_watermark_path)

        await websocket_manager.broadcast("Watermarking process completed successfully!")

        return {
            "message": "Watermarking successful",
            "watermarked_image": watermarked_image_base64,
            "watermark_ipfs_hash": watermark_ipfs_hash,
            "blockchain_tx_hash": blockchain_tx_hash,
        }
    except Exception as e:
        await websocket_manager.broadcast(f"Error: {str(e)}")
        raise e
    
@app.post("/api/verify")
async def verify_watermark(watermarked_image: UploadFile = File(...),transaction_hash: str = Form(...),):
    try:
        if not transaction_hash:
            await websocket_manager.broadcast("Error: Transaction hash is required")
            return {"error": "Transaction hash is required"}

        # Save the uploaded watermarked image temporarily
        watermarked_image_path = f"temp_{watermarked_image.filename}"
        await websocket_manager.broadcast("Saving uploaded watermarked image...")
        with open(watermarked_image_path, "wb") as f:
            f.write(await watermarked_image.read())

        try:
            # Retrieve IPFS hash from the blockchain
            await websocket_manager.broadcast("Retrieving IPFS hash from blockchain...")
            from read_ipfs_hash import get_ipfs_hash_from_transaction
            ipfs_hash = get_ipfs_hash_from_transaction(transaction_hash)

            # Download the watermark from IPFS
            await websocket_manager.broadcast("Downloading watermark from IPFS...")
            from download import download_from_ipfs
            downloaded_watermark_path = "downloaded_actual_watermark.png"
            download_from_ipfs(ipfs_hash)

            # Extract the watermark from the uploaded watermarked image
            await websocket_manager.broadcast("Extracting watermark from uploaded image...")
            from extract import extract_lsb_watermark
            extracted_watermark_path = "extracted_watermark.png"
            extract_lsb_watermark(watermarked_image_path)

            # Perform XOR verification
            await websocket_manager.broadcast("Performing XOR verification...")
            from verify import verify_watermark
            verification_result = verify_watermark(
                downloaded_path=downloaded_watermark_path,
                extracted_path=extracted_watermark_path,
            )

            # Clean up temporary files
            os.remove(watermarked_image_path)
            os.remove(downloaded_watermark_path)
            os.remove(extracted_watermark_path)

            await websocket_manager.broadcast("Verification process completed successfully!")

            return {"message": verification_result}

        except Exception as e:
            # Clean up temporary files in case of an error
            if os.path.exists(watermarked_image_path):
                os.remove(watermarked_image_path)
            if os.path.exists("downloaded_actual_watermark.png"):
                os.remove("downloaded_actual_watermark.png")
            if os.path.exists("extracted_watermark.png"):
                os.remove("extracted_watermark.png")

            await websocket_manager.broadcast(f"Error: {str(e)}")
            return {"error": str(e)}
    except Exception as e:
        await websocket_manager.broadcast(f"Error: {str(e)}")
        raise e