import React, { useState } from "react";
import { useDropzone } from "react-dropzone";
import "./UploadPage.css";

const UploadPage: React.FC = () => {
  const [medicalImage, setMedicalImage] = useState<File | null>(null);
  const [watermarkImage, setWatermarkImage] = useState<File | null>(null);
  const [ipfsHash, setIpfsHash] = useState<string | null>(null);

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

    try {
      const response = await fetch("http://localhost:5000/api/watermark", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setIpfsHash(data.ipfs_hash);
      alert("Upload successful!");
    } catch (error) {
      console.error("Error uploading:", error);
      alert("Upload failed.");
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

        {ipfsHash && (
          <div className="upload-result">
            <p><strong>IPFS Hash:</strong> {ipfsHash}</p>
            <a
              href={`https://ipfs.io/ipfs/${ipfsHash}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              View on IPFS
            </a>
          </div>
        )}
      </main>
    </div>
  );
};

export default UploadPage;