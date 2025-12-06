"use client";

import React, { useState } from "react";
import JobCard from "./JobCard";
import JobModal from "./JobModal";

interface Job {
  company_name: string;
  title: string;
  description: string;
  max_salary: number;
  location: string;
  job_url: string;
}

interface JobListProps {
  jobs: Job[];
  currentIndex: number;
  onIndexChange: (newIndex: number) => void;
  jobsPerPage?: number;
}

export default function JobList({
  jobs,
  currentIndex,
  onIndexChange,
  jobsPerPage = 20,
}: JobListProps) {
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Get the jobs for the current page
  const currentJobs = jobs.slice(currentIndex, currentIndex + jobsPerPage);
  const totalPages = Math.ceil(jobs.length / jobsPerPage);
  const currentPage = Math.floor(currentIndex / jobsPerPage);

  const handleJobClick = (job: Job) => {
    setSelectedJob(job);
    setIsModalOpen(true);
  };

  const handleNextPage = () => {
    const nextIndex = currentIndex + jobsPerPage;
    if (nextIndex < jobs.length) {
      onIndexChange(nextIndex);
    }
  };

  const handlePreviousPage = () => {
    const prevIndex = currentIndex - jobsPerPage;
    if (prevIndex >= 0) {
      onIndexChange(prevIndex);
    }
  };

  const handlePageJump = (pageNumber: number) => {
    onIndexChange(pageNumber * jobsPerPage);
  };

  if (jobs.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">No jobs found. Upload a resume to get started!</p>
      </div>
    );
  }

  return (
    <div>
      {/* Job Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        {currentJobs.map((job, index) => (
          <JobCard
            key={index}
            job={job}
            onClick={() => handleJobClick(job)}
          />
        ))}
      </div>

      {/* Job Modal */}
      <JobModal
        job={selectedJob}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div className="flex justify-center items-center gap-2 mb-8">
          {/* Previous Button */}
          <button
            onClick={handlePreviousPage}
            disabled={currentIndex === 0}
            className="px-4 py-2 bg-gray-300 text-gray-800 rounded-lg font-semibold hover:bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            ← Previous
          </button>

          {/* Page Numbers */}
          <div className="flex gap-1">
            {Array.from({ length: totalPages }).map((_, pageNum) => (
              <button
                key={pageNum}
                onClick={() => handlePageJump(pageNum)}
                className={`px-3 py-2 rounded-lg font-semibold transition-colors ${
                  currentPage === pageNum
                    ? "bg-blue-600 text-white"
                    : "bg-gray-200 text-gray-800 hover:bg-gray-300"
                }`}
              >
                {pageNum + 1}
              </button>
            ))}
          </div>

          {/* Next Button */}
          <button
            onClick={handleNextPage}
            disabled={currentIndex + jobsPerPage >= jobs.length}
            className="px-4 py-2 bg-gray-300 text-gray-800 rounded-lg font-semibold hover:bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Next →
          </button>
        </div>
      )}

      {/* Page Info */}
      <div className="text-center text-gray-600">
        <p>
          Showing {currentIndex + 1}-{Math.min(currentIndex + jobsPerPage, jobs.length)} of{" "}
          {jobs.length} jobs
        </p>
      </div>
    </div>
  );
}
