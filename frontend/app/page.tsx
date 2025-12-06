"use client";

import axios from "axios";
import React, {useState} from "react";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const onFileChange = (event) => {
    const file = event.target.files[0];

    if (file && file.type !== "application/pdf") {
      setMessage("❌ Please select a PDF file");
      setSelectedFile(null);
      return;
    }

    setSelectedFile(event.target.files[0]);
    setMessage("");

  };

  const onFileUpload = async () => {
    if (!selectedFile) {
      setMessage("❌ Please select a file first");
      return;
    }

    const formData = new FormData();
    formData.append(
      "resume",
      selectedFile,
      selectedFile.name
    );
    console.log(selectedFile);
    let result = await axios.post("http://127.0.0.1:8000/jobs", formData);

  };


  return (
    <main className="flex flex-col items-center justify-center p-8 min-h-screen">
      <h1 className="text-5xl mb-8">
        ND DataClub - LinkedIn
      </h1>
      
      <div className="border-2 border-dashed border-gray-300 p-8 rounded-lg w-full max-w-md">
        <h3 className="text-xl font-bold mb-4">Upload a Resume (PDF)</h3>
        
        <input 
          type="file" 
          accept=".pdf"
          onChange={onFileChange}
          disabled={loading}
          className="mb-4 p-2 border border-gray-300 rounded w-full"
        />
        
        {selectedFile && (
          <p className="text-sm text-gray-600 mb-4">
            Selected: {selectedFile.name}
          </p>
        )}
        
        <button 
          onClick={onFileUpload}
          disabled={loading || !selectedFile}
          className="w-full bg-blue-600 text-white py-2 rounded font-bold hover:bg-blue-700 disabled:bg-gray-400"
        >
          {loading ? "Uploading..." : "Upload"}
        </button>

        {message && (
          <p className="mt-4 text-center font-semibold">
            {message}
          </p>
        )}
      </div>
    </main>
  );
}