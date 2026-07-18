// Handles audio file upload and initiates backend processing pipeline
import React, { useState } from "react";

// Captures user audio input, sends it to API, and triggers async job processing
function UploadAudio({ setJobId, setStatus }) {
  // Stores selected audio file from user input
  const [file, setFile] = useState(null);

  // Sends audio file to backend and starts processing workflow
  const handleUpload = async () => {
    // Prevent upload if no file is selected
    if (!file) return alert("Please select a file first!");

    // Update UI to show processing state immediately
    setStatus("processing");

    // Prepare multipart form data for file upload
    const formData = new FormData();
    formData.append("file", file);

    // Call backend API to upload audio and enqueue processing job
    const res = await fetch("http://127.0.0.1:8000/summarize-audio", {
      method: "POST",
      headers: {
        "x-api-key": "supersecret123"
      },
      body: formData
    });

    // Extract job ID to track processing status asynchronously
    const data = await res.json();
    // Store job ID so UI can start polling for results
    setJobId(data.job_id);
  };

  return (
    <div className="upload-box">

      {/* File input for selecting audio to upload */}
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />

      {/* Triggers upload and processing pipeline */}
      <button onClick={handleUpload}>Upload</button>

    </div>
  );
}
export default UploadAudio;