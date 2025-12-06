from fastapi import FastAPI,  UploadFile, File
from pydantic import BaseModel

import fitz # pymufdf

app = FastAPI()




@app.get("/")
async def root():
  return {"message": "Hello"}

app.post("/get_jobs")
async def get_jobs(file: UploadFile = File(...)):
  contents = await file.read()

  pdf = fitz.open(stream=contents, filetype = "pdf")
  text = "" 
  for page in pdf:
    text += page.get_text()
  # call the parser

  # query the database for job postings

  # return a json with the top jobs

  return {"message": "Here are the jobs"}

# Point of communcation between:
# 1. Helper Functions
# 2. Frontend