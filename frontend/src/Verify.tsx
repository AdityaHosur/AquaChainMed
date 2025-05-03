import React, { useState } from "react";
import { useDropzone } from "react-dropzone";
import "./Verify.css";

const Verify: React.FC = () => {
  const [watermarkImage, setWatermarkImage] = useState<File | null>(null);
  const [transactionHash, setTransactionHash] = useState<string>("");
  const [loadingMessage, setLoadingMessage] = useState<string>("");
  const [verificationResult, setVerificationResult] = useState<string | null>(null);

  const handleWatermarkDrop = (acceptedFiles: File[]) => {
    setWatermarkImage(acceptedFiles[0]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!watermarkImage || !transactionHash) {
      alert("Please upload a watermark image and enter the transaction hash.");
      return;
    }
    const formattedTransactionHash = transactionHash.startsWith("0x")
    ? transactionHash
    : `0x${transactionHash}`;
    const formData = new FormData();
    formData.append("watermarked_image", watermarkImage);
    formData.append("transaction_hash", formattedTransactionHash);

    // Connect to WebSocket
    const ws = new WebSocket("ws://127.0.0.1:8000/ws");

    ws.onopen = () => {
      console.log("WebSocket connection established");
      setLoadingMessage("Starting verification process...");
    };

    ws.onmessage = (event) => {
      console.log("WebSocket message received:", event.data);
      setLoadingMessage(event.data); // Update the loading message
    };

    ws.onclose = () => {
      console.log("WebSocket connection closed");
      setLoadingMessage("");
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/api/verify", {
        method: "POST",
        body: formData,
      });
  
      const data = await response.json();
      if (data.message) {
        setVerificationResult(data.message);
      } else if (data.error) {
        setVerificationResult(`Error: ${data.error}`); // Set the error in the state
      }
    } catch (error) {
      console.error("Error verifying watermark:", error);
      setVerificationResult("Verification failed"); // Set the error in the state
    }finally {
      ws.close(); // Close the WebSocket connection
    }
  };

  const watermarkDropzone = useDropzone({
    onDrop: handleWatermarkDrop,
    accept: { "image/*": [] },
    multiple: false,
  });

  return (
    <div className="verify-page">
      <main className="verify-main">
        <form className="verify-form" onSubmit={handleSubmit}>
          <div className="verify-card">
            <h2>Verify Watermark</h2>

            {/* Watermark Image Upload */}
            <div
              className="verify-drag-area"
              {...watermarkDropzone.getRootProps()}
            >
              <input {...watermarkDropzone.getInputProps()} />
              <p>Drag & Drop your watermark image here, or click to browse</p>
              {watermarkImage && (
                <p className="file-name">Selected: {watermarkImage.name}</p>
              )}
            </div>

            {/* Transaction Hash Input */}
            <div className="transaction-hash-input">
              <label htmlFor="transactionHash">Transaction Hash</label>
              <input
                type="text"
                id="transactionHash"
                placeholder="Enter transaction hash"
                value={transactionHash}
                onChange={(e) => setTransactionHash(e.target.value)}
              />
            </div>

            <button type="submit" className="verify-button">
              Verify
            </button>
          </div>
        </form>
        {loadingMessage && (
          <div className="loader-container">
            <div className="spinner"></div>
            <p className="loader-message">{loadingMessage}</p>
          </div>
        )}

        {/* Verification Result */}
        {verificationResult && (
          <div className="verification-result">
            <h3>Verification Result</h3>
            <p>{verificationResult}</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default Verify;