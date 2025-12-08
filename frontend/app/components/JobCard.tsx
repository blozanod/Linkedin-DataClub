"use client";

import React from "react";

interface Job {
  company_name: string;
  title: string;
  description: string;
  max_salary: number;
  location: string;
  //tags?: string[];
  job_url: string;
}

interface JobCardProps {
  job: Job;
  onClick: () => void;
}

export default function JobCard({ job, onClick }: JobCardProps) {
  return (
    <div
      onClick={onClick}
      className="bg-white rounded-lg shadow-md p-6 cursor-pointer hover:shadow-lg hover:scale-105 transition-all duration-200 border border-gray-200"
    >
      <h3 className="text-xl font-bold text-gray-800 mb-2">{job.title}</h3>
      <p className="text-gray-600 font-semibold mb-2">{job.company_name}</p>
      <p className="text-gray-500 text-sm mb-2">📍 {job.location || 'Location not shown'}</p>
      {job.max_salary > 0 ? (
        <p className="text-green-600 font-semibold">💰 ${job.max_salary.toLocaleString()}</p>
      ) : (
        <p className="text-sm text-gray-400">Salary not shown</p>
      )}

      {/* Tags removed from card display per UI preference */}
    </div>
  );
}
