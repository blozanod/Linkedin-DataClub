import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base, Session as SessionType
from sqlalchemy import JSON
import os

# Path to this script
HELPER_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to Databases folder, which is one directory up
RESUME_DIR = os.path.join(HELPER_DIR, "..", "Databases")
JOBS_DIR = os.path.join(HELPER_DIR, "..", "Scraping")

# Normalize the path
RESUME_DIR = os.path.abspath(RESUME_DIR)
JOBS_DIR = os.path.abspath(JOBS_DIR)

# Final Paths
RESUME_PATH = os.path.join(RESUME_DIR, "resumes.db")
JOBS_PATH = os.path.join(JOBS_DIR, "jobs.db")

# Postings Session
postings_db = sa.create_engine(f"sqlite:///{JOBS_PATH}")
Session_Posting = sessionmaker(bind=postings_db) # functions as the workspace
Base_Posting = declarative_base()

# Resumes Session
resumes_db = sa.create_engine(f"sqlite:///{RESUME_PATH}")
Session_Resume = sessionmaker(bind=resumes_db) # functions as the workspace
Base_Resume = declarative_base()

class Posting(Base_Posting):
  __tablename__ = "remoteokjobs"

  job_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
  company_name: Mapped[str]
  title: Mapped[str]
  description: Mapped[str]
  keywords: Mapped[list] = mapped_column(JSON)
  max_salary: Mapped[int]
  location: Mapped[str]
  job_url: Mapped[str]
  tags: Mapped[list] = mapped_column(JSON)

  def __repr__(self) -> str:
    return f"<Posting(company_name={self.company_name}, title={self.title})>"

class Resume(Base_Resume):
  __tablename__ = "resumes"

  ID: Mapped[int] = mapped_column(primary_key=True, unique=True)
  Resume_str: Mapped[str]
  Resume_html: Mapped[str]
  Category: Mapped[str]

  def __repr__(self) -> str:
    return f"<Resume(ID={self.ID}, Category={self.Category})>"