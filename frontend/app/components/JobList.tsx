"use client";

import React, { useState, useEffect, useRef } from "react";
import JobCard from "./JobCard";
import JobModal from "./JobModal";

interface Job {
  company_name: string;
  title: string;
  description: string;
  max_salary: number;
  location: string;
  tags?: string[];
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
  const [overflowSelect, setOverflowSelect] = useState<string>("");
  const [locationFilter, setLocationFilter] = useState<string>("All");
  const [internshipFilter, setInternshipFilter] = useState<"all" | "only" | "exclude">("all");
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [hasLocationOnly, setHasLocationOnly] = useState(false);
  const [hasSalaryOnly, setHasSalaryOnly] = useState(false);
  const [showTagsDropdown, setShowTagsDropdown] = useState(false);
  const tagsDropdownRef = useRef<HTMLDivElement | null>(null);

  // derive available filter options
  const uniqueLocations = Array.from(new Set(jobs.map((j) => (j.location || "")).filter(Boolean)));
  const fallbackTags = Array.from(new Set(jobs.flatMap((j) => (j as any).tags || [])));
  const [availableTags, setAvailableTags] = useState<string[]>(fallbackTags);

  // Fetch canonical tag list from backend and use it as the only tags shown in the filter.
  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/tags");
        if (!res.ok) return;
        const data = await res.json();
        if (data && Array.isArray(data.tags) && !cancelled) {
          setAvailableTags(data.tags);
        }
      } catch (e) {
        // If the backend tags endpoint is not available, keep using fallback tags.
        console.warn("Could not fetch /tags, using fallback tags.", e);
      }
    })();
    return () => { cancelled = true; };
  }, []);

  // helper to detect internship postings
  const isInternship = (job: Job) => {
    const titleIntern = job.title?.toLowerCase().includes("intern");
    const tags = (job as any).tags || [];
    const tagIntern = tags.some((t: string) => t.toLowerCase().includes("intern"));
    return titleIntern || tagIntern;
  };

  // Apply filters
  const filteredJobs = jobs
    .filter((job) => {
      if (locationFilter !== "All" && (job.location || "") !== locationFilter) return false;

      if (internshipFilter === "only" && !isInternship(job)) return false;
      if (internshipFilter === "exclude" && isInternship(job)) return false;

      if (selectedTags.length > 0) {
        const tags = (job as any).tags || [];
        // match if job has any of the selected tags
        if (!selectedTags.some((t) => tags.map(String).includes(t))) return false;
      }

      if (hasLocationOnly && !(job.location && job.location.trim().length > 0)) return false;

      if (hasSalaryOnly && !(job.max_salary && job.max_salary > 0)) return false;

      return true;
    })
    .slice();

  // Preserve backend ordering: do not sort jobs on the client.

  const totalPages = Math.ceil(filteredJobs.length / jobsPerPage);
  const currentPage = Math.floor(currentIndex / jobsPerPage);

  const handleJobClick = (job: Job) => {
    setSelectedJob(job);
    setIsModalOpen(true);
  };

  const handleNextPage = () => {
    const nextIndex = currentIndex + jobsPerPage;
    if (nextIndex < filteredJobs.length) {
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

  // reset index when filters change
  useEffect(() => {
    onIndexChange(0);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [locationFilter, internshipFilter, selectedTags.join(','), hasLocationOnly, hasSalaryOnly]);

  // close tags dropdown on outside click
  useEffect(() => {
    const onDocClick = (e: MouseEvent) => {
      if (tagsDropdownRef.current && !tagsDropdownRef.current.contains(e.target as Node)) {
        setShowTagsDropdown(false);
      }
    };
    document.addEventListener("mousedown", onDocClick);
    return () => document.removeEventListener("mousedown", onDocClick);
  }, []);

  if (jobs.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">No jobs found. Upload a resume to get started!</p>
      </div>
    );
  }
  // derive the page slice from filteredJobs
  const pageStart = currentIndex;
  const pageSlice = filteredJobs.slice(pageStart, pageStart + jobsPerPage);

  return (
    <div>
      {/* Filters */}
      <div className="bg-white p-4 rounded-lg mb-6 border border-gray-200 text-gray-800">
        <div className="flex flex-wrap gap-3 items-center">
          <div className="flex items-center gap-2">
            <label className="font-semibold text-gray-800">Location:</label>
            <select
              value={locationFilter}
              onChange={(e) => setLocationFilter(e.target.value)}
              className="px-2 py-1 rounded border border-gray-300 bg-white text-gray-800"
            >
              <option value="All">All</option>
              {uniqueLocations.map((loc) => (
                <option key={loc} value={loc}>{loc}</option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-2">
            <label className="font-semibold text-gray-800">Internship:</label>
            <select
              value={internshipFilter}
              onChange={(e) => setInternshipFilter(e.target.value as any)}
              className="px-2 py-1 rounded border border-gray-300 bg-white text-gray-800"
            >
              <option value="all">All</option>
              <option value="only">Internships only</option>
              <option value="exclude">Exclude internships</option>
            </select>
          </div>

          <div className="flex items-center gap-2" ref={tagsDropdownRef}>
            <label className="font-semibold text-gray-800">Tags:</label>
            <div className="relative">
              <button
                type="button"
                onClick={() => setShowTagsDropdown((s) => !s)}
                className="px-3 py-1 rounded border border-gray-300 bg-white text-gray-800 min-w-[160px] text-left"
              >
                {selectedTags.length > 0 ? `${selectedTags.length} selected` : "Select tags"}
              </button>

              {showTagsDropdown && (
                <div className="absolute z-10 mt-2 w-64 max-h-56 overflow-auto bg-white border border-gray-200 rounded shadow-md p-2">
                  {availableTags.map((t) => (
                    <label key={t} className="flex items-center gap-2 px-2 py-1 hover:bg-gray-50">
                      <input
                        type="checkbox"
                        checked={selectedTags.includes(t)}
                        onChange={(e) => {
                          if (e.target.checked) setSelectedTags((s) => [...s, t]);
                          else setSelectedTags((s) => s.filter((x) => x !== t));
                        }}
                      />
                      <span className="text-sm">{t}</span>
                    </label>
                  ))}

                  <div className="flex justify-between items-center mt-2 px-2">
                    <button
                      type="button"
                      onClick={() => { setSelectedTags([]); setShowTagsDropdown(false); }}
                      className="text-sm text-gray-600"
                    >
                      Clear
                    </button>
                    <button
                      type="button"
                      onClick={() => setShowTagsDropdown(false)}
                      className="text-sm text-blue-600"
                    >
                      Done
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="flex items-center gap-2">
            <label className="font-semibold text-gray-800">Has:</label>
            <label className="flex items-center gap-1 text-gray-800"><input type="checkbox" checked={hasLocationOnly} onChange={(e) => setHasLocationOnly(e.target.checked)} /> Location</label>
            <label className="flex items-center gap-1 text-gray-800"><input type="checkbox" checked={hasSalaryOnly} onChange={(e) => setHasSalaryOnly(e.target.checked)} /> Salary</label>
          </div>

          {/* salary sort removed to preserve backend ordering */}
        </div>
      </div>

      {/* Job Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        {pageSlice.map((job, index) => (
          <JobCard
            key={pageStart + index}
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

              {/* Page Numbers: current page first, then next two pages */}
              <div className="flex gap-1 items-center">
                {(() => {
                  const pagesToShow: number[] = [];
                  for (let p = currentPage; p <= currentPage + 2 && p < totalPages; p++) {
                    pagesToShow.push(p);
                  }

                  const lastShown = pagesToShow.length ? pagesToShow[pagesToShow.length - 1] : -1;
                  const remainingPages: number[] = [];
                  for (let p = lastShown + 1; p < totalPages; p++) remainingPages.push(p);

                  return (
                    <>
                      {pagesToShow.map((p) => (
                        <button
                          key={p}
                          onClick={() => handlePageJump(p)}
                          className={`px-3 py-2 rounded-lg font-semibold transition-colors ${
                            currentPage === p
                              ? "bg-blue-600 text-white"
                              : "bg-gray-200 text-gray-800 hover:bg-gray-300"
                          }`}
                        >
                          {p + 1}
                        </button>
                      ))}

                      {remainingPages.length > 0 && (
                        <select
                          value={overflowSelect}
                          onChange={(e) => {
                            const v = e.target.value;
                            setOverflowSelect(v);
                            if (v !== "") {
                              handlePageJump(Number(v));
                              setOverflowSelect("");
                            }
                          }}
                          className="px-3 py-2 rounded-lg bg-gray-200 text-gray-800 font-semibold hover:bg-gray-300"
                          aria-label="More pages"
                        >
                          <option value="">More...</option>
                          {remainingPages.map((p) => (
                            <option key={p} value={p}>
                              {p + 1}
                            </option>
                          ))}
                        </select>
                      )}
                    </>
                  );
                })()}
              </div>

              {/* Next Button */}
              <button
                onClick={handleNextPage}
                disabled={currentIndex + jobsPerPage >= filteredJobs.length}
                className="px-4 py-2 bg-gray-300 text-gray-800 rounded-lg font-semibold hover:bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Next →
              </button>
            </div>
          )}

      {/* Page Info */}
      {filteredJobs.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-gray-500">No jobs match the current filters.</p>
        </div>
      ) : (
        <div className="text-center text-gray-700">
          <p>
            Showing {Math.min(filteredJobs.length, pageStart + 1)}-{Math.min(pageStart + jobsPerPage, filteredJobs.length)} of {filteredJobs.length} jobs
          </p>
        </div>
      )}
    </div>
  );
}
