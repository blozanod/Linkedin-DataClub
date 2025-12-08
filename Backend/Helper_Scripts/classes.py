import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base, Session as SessionType
from sqlalchemy import JSON
from sqlalchemy.pool import NullPool
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
# Use NullPool and disable check_same_thread to avoid SQLite "database is locked"
# errors when multiple threads access the DB (background scraper + web requests).
postings_db = sa.create_engine(
  f"sqlite:///{JOBS_PATH}",
  connect_args={"check_same_thread": False},
  poolclass=NullPool,
)
Session_Posting = sessionmaker(bind=postings_db)
Base_Posting = declarative_base()

# Resumes Session
resumes_db = sa.create_engine(
  f"sqlite:///{RESUME_PATH}",
  connect_args={"check_same_thread": False},
  poolclass=NullPool,
)
Session_Resume = sessionmaker(bind=resumes_db)
Base_Resume = declarative_base()

class Posting(Base_Posting):
  __tablename__ = "remoteokjobs"

  job_id: Mapped[str] = mapped_column(primary_key=True, unique=True)
  company_name: Mapped[str]
  title: Mapped[str]
  title_keywords: Mapped[list] = mapped_column(JSON)
  description: Mapped[str]
  keywords: Mapped[list] = mapped_column(JSON)
  max_salary: Mapped[int]
  location: Mapped[str]
  job_url: Mapped[str]
  tags: Mapped[list] = mapped_column(JSON)
  tags_keywords: Mapped[list] = mapped_column(JSON)

  def __repr__(self) -> str:
    return f"<Posting(company_name={self.company_name}, title={self.title})>"
  
  def to_dict(self):
        return {
            'company_name': self.company_name,
            'title': self.title,
            'description': self.description,
            'max_salary': self.max_salary,
        'location': self.location,
        'job_url': self.job_url,
        'tags': self.tags if self.tags is not None else [],
        }

class Resume(Base_Resume):
  __tablename__ = "resumes"

  ID: Mapped[int] = mapped_column(primary_key=True, unique=True)
  Resume_str: Mapped[str]
  Resume_html: Mapped[str]
  Category: Mapped[str]

  def __repr__(self) -> str:
    return f"<Resume(ID={self.ID}, Category={self.Category})>"