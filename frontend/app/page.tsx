"use client";

import axios from "axios";
import React, { useState } from "react";
import JobList from "./components/JobList";

interface Job {
  company_name: string;
  title: string;
  description: string;
  max_salary: number;
  location: string;
  job_url: string;
}

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [index, setIndex] = useState(0);
  const [message, setMessage] = useState("");
  const [jobs, setJobs] = useState<Job[]>([]);
  const [hasSearched, setHasSearched] = useState(false);

  const onFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];

    if (file && file.type !== "application/pdf") {
      setMessage("❌ Please select a PDF file");
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file || null);
    setMessage("");
  };

  const onFileUpload = async () => {
    if (!selectedFile) {
      setMessage("❌ Please select a file first");
      return;
    }

    try {
      setLoading(true);
      const formData = new FormData();
      formData.append("file", selectedFile, selectedFile.name);
      formData.append("index", String(index));

      const result = await axios.post(
        "http://127.0.0.1:8000/get_jobs",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setJobs(result.data.jobs || []);
      setHasSearched(true);
      setIndex(0);
      setMessage("✅ Resume processed successfully!");
    } catch (error) {
      setMessage("❌ Error processing resume. Please try again.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex flex-col items-center p-8 min-h-screen bg-gray-50">
      <h1 className="text-5xl font-bold mb-2 text-gray-800">
        ND DataClub - LinkedIn
      </h1>
      <p className="text-gray-600 mb-8">Find jobs that match your resume</p>

      {/* Upload Section */}
      <div className="border-2 border-dashed border-gray-300 p-8 rounded-lg w-full max-w-md bg-white mb-12">
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
          className="w-full bg-blue-600 text-white py-2 rounded font-bold hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
        >
          {loading ? "Uploading..." : "Upload"}
        </button>

        {message && (
          <p className="mt-4 text-center font-semibold">
            {message}
          </p>
        )}
      </div>

      {/* Job Results Section */}
      {hasSearched && (
        <div className="w-full">
          <JobList
            jobs={jobs}
            currentIndex={index}
            onIndexChange={setIndex}
            jobsPerPage={20}
          />
        </div>
      )}
    </main>
  );
}