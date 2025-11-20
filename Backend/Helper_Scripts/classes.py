import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base, Session as SessionType
from sqlalchemy import and_

# starting up the database 

postings_db = sa.create_engine(r"sqlite:///C:\Users\bfcla\Programming Projects\DataClub\Linkedin-DataClub\Backend\Databases\postings.db") # THIS WILL CHANGE BASED ON WINDOWS/MAC
Session = sessionmaker(bind=postings_db) # functions as the workspace
Base = declarative_base()

class Posting(Base):
  __tablename__ = "postings"

  job_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
  company_name: Mapped[str]
  title: Mapped[str]
  description: Mapped[str]
  max_salary: Mapped[int]
  pay_period: Mapped[str]
  location: Mapped[str]
  company_id: Mapped[str]
  views: Mapped[int]
  med_salary: Mapped[int]
  min_salary: Mapped[int]
  """
  formatted_work_type: Mapped[str]
  applies: Mapped[int]
  original_listed_time: Mapped[int]
  remote_allowed: Mapped[int]
  job_posting_url: Mapped[str]
  application_url: Mapped[str]
  application_type: Mapped[str]
  expiry: Mapped[int]
  closed_time: Mapped[int]
  formatted_experience_level: Mapped[str]
  skills_desc: Mapped[str]
  listed_time: Mapped[int]
  posting_domain: Mapped[str]
  sponsored: Mapped[int]
  work_type: Mapped[str]
  currency: Mapped[str]
  compensation_type: Mapped[str]
  normalized_salary: Mapped[int]
  zip_code: Mapped[int]
  fips: Mapped[int]
  """

  def __repr__(self) -> str:
    return f"<Posting(company_name={self.company_name}, title={self.title})>"

  class Resume(Base):
    __tablename__ = "resumes"

    ID: Mapped[int] = mapped_column(primary_key=True, unique=True)
    Resume_str: Mapped[str]
    Resume_html: Mapped[str]
    Category: Mapped[str]