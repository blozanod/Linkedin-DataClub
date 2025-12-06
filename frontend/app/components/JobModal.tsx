"use client";

import React from "react";

interface Job {
  company_name: string;
  title: string;
  description: string;
  max_salary: number;
  location: string;
  job_url: string;
}

interface JobModalProps {
  job: Job | null;
  isOpen: boolean;
  onClose: () => void;
}

export default function JobModal({ job, isOpen, onClose }: JobModalProps) {
  if (!isOpen || !job) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-gradient-to-r from-blue-600 to-blue-800 text-white p-6 flex justify-between items-start">
          <div>
            <h2 className="text-3xl font-bold mb-2">{job.title}</h2>
            <p className="text-xl text-blue-100">{job.company_name}</p>
          </div>
          <button
            onClick={onClose}
            className="text-2xl font-bold hover:text-gray-300"
          >
            ✕
          </button>
        </div>

        <div className="p-6">
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div>
              <h3 className="text-gray-600 font-semibold">Location</h3>
              <p className="text-lg text-gray-800">{job.location}</p>
            </div>
            <div>
              <h3 className="text-gray-600 font-semibold">Max Salary</h3>
              <p className="text-lg text-green-600 font-bold">
                {job.max_salary > 0 ? `$${job.max_salary.toLocaleString()}` : "Not specified"}
              </p>
            </div>
          </div>

          <div className="mb-6">
            <h3 className="text-gray-600 font-semibold mb-2">Description</h3>
            <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">
              {job.description}
            </p>
          </div>

          <div className="flex gap-4">
            <a
              href={job.job_url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 transition-colors text-center"
            >
              Apply Now
            </a>
            <button
              onClick={onClose}
              className="flex-1 bg-gray-300 text-gray-800 py-3 px-6 rounded-lg font-semibold hover:bg-gray-400 transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
