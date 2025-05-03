import React, { useState } from "react";
import { useDropzone } from "react-dropzone";
import "./UploadPage.css";

const UploadPage: React.FC = () => {
  const [medicalImage, setMedicalImage] = useState<File | null>(null);
  const [watermarkImage, setWatermarkImage] = useState<File | null>(null);
  const [watermarkedImage, setWatermarkedImage] = useState<string | null>(null);
  const [watermarkIpfsHash, setWatermarkIpfsHash] = useState<string | null>(null);
  const [blockchainTxHash, setBlockchainTxHash] = useState<string | null>(null);
  const [loadingMessage, setLoadingMessage] = useState<string>("");
  const handleMedicalDrop = (acceptedFiles: File[]) => {
    setMedicalImage(acceptedFiles[0]);
  };

  const handleWatermarkDrop = (acceptedFiles: File[]) => {
    setWatermarkImage(acceptedFiles[0]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!medicalImage || !watermarkImage) {
      alert("Please select both images.");
      return;
    }

    const formData = new FormData();
    formData.append("medical_image", medicalImage);
    formData.append("watermark_image", watermarkImage);

    const ws = new WebSocket("ws://127.0.0.1:8000/ws");
    ws.onopen = () => {
      console.log("WebSocket connection established for watermarking");
      setLoadingMessage("Starting watermarking process...");
      ws.send("start_watermarking"); // Notify backend to start the process
    };

    ws.onmessage = (event) => {
      console.log("WebSocket message received:", event.data);
      setLoadingMessage(event.data); // Update the loading message
    };

    ws.onclose = () => {
      console.log("WebSocket connection closed");
      setLoadingMessage("");
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      alert("An error occurred during the watermarking process.");
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/api/watermark", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (data.watermarked_image) {
        setWatermarkedImage(`data:image/png;base64,${data.watermarked_image}`);
        setWatermarkIpfsHash(data.watermark_ipfs_hash);
        setBlockchainTxHash(data.blockchain_tx_hash);
      } else {
        alert("Watermarking failed.");
      }
    } catch (error) {
      console.error("Error uploading:", error);
      alert("Upload failed.");
    }finally {
      ws.close(); // Close the WebSocket connection
    }
  };

  const medicalDropzone = useDropzone({
    onDrop: handleMedicalDrop,
    accept: { "image/*": [] },
    multiple: false,
  });

  const watermarkDropzone = useDropzone({
    onDrop: handleWatermarkDrop,
    accept: { "image/*": [] },
    multiple: false,
  });

  return (
    <div className="upload-page">
      <main className="upload-main">
        <form className="upload-form" onSubmit={handleSubmit}>
          <div className="upload-cards">
            {/* Medical Image Upload Card */}
            <div className="upload-card">
            <h2>Medical Image</h2>
            <div
              className="upload-drag-area"
              {...medicalDropzone.getRootProps()}
            >
              <input {...medicalDropzone.getInputProps()} />
              <p>Drag & Drop your medical image here, or click to browse</p>
              {medicalImage && (
                <p className="file-name">Selected: {medicalImage.name}</p>
              )}
            </div>
          </div>

            {/* Watermark Image Upload Card */}
            <div className="upload-card">
            <h2>Watermark Image</h2>
            <div
              className="upload-drag-area"
              {...watermarkDropzone.getRootProps()}
            >
              <input {...watermarkDropzone.getInputProps()} />
              <p>Drag & Drop your watermark image here, or click to browse</p>
              {watermarkImage && (
                <p className="file-name">Selected: {watermarkImage.name}</p>
              )}
            </div>
          </div>
          </div>

          <button type="submit">Upload & Watermark</button>
        </form>
        {loadingMessage && (
          <div className="loader-container">
            <div className="spinner"></div>
            <p className="loader-message">{loadingMessage}</p>
          </div>
        )}
              {watermarkedImage && (
        <div className="upload-result">
          <h3>Watermarked Image</h3>
          <div className="watermarked-image-container">
            <img src={watermarkedImage} alt="Watermarked" className="watermarked-image" />
          </div>
          <p className="ipfs-link">
            <strong>Watermark IPFS Hash:</strong>{" "}
            <a
              href={`https://ipfs.io/ipfs/${watermarkIpfsHash}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              {watermarkIpfsHash}
            </a>
          </p>
          <p className="blockchain-link">
              <strong>Blockchain Transaction Hash:</strong>{" "}
              <a
                href={`https://sepolia.etherscan.io/tx/0x${blockchainTxHash}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                {blockchainTxHash}
              </a>
            </p>
            <button
            className="download-button"
            onClick={() => {
              const link = document.createElement("a");
              link.href = watermarkedImage;
              link.download = "watermarked_image.png";
              link.click();
            }}
          >
            Download Watermarked Image
          </button>
        </div>
      )}
      </main>
    </div>
  );
};

export default UploadPage;