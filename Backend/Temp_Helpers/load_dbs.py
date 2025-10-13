import pandas as pd
import sqlite3

# Load Job Postings
# https://www.kaggle.com/datasets/arshkon/linkedin-job-postings
df = pd.read_csv("../Databases/postings.csv")

conn = sqlite3.connect("../Databases/postings.db")

df.to_sql("postings", con = conn, if_exists="replace", index=False)

conn.close()

# Load Resumes
# https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
df = pd.read_csv("../Databases/resume.csv")

conn = sqlite3.connect("../Databases/resumes.db")

df.to_sql("resumes", con = conn, if_exists="replace", index=False)

conn.close()