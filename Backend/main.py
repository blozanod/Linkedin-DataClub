from fastapi import FastAPI, UploadFile, File, Form
import fitz  # pymupdf
from Helper_Scripts import parsing
import json

app = FastAPI()

@app.get("/")
async def root():
  return {"message": "Hello"}

@app.post("/get_jobs")
async def get_jobs(file: UploadFile = File(...), index: int = Form(...)):
  """
  Upload a PDF resume and get job recommendations
  
  Parameters:
  - file: PDF file
  - index: Starting index for job results
  """
 
  # Read PDF file
  contents = await file.read()
  
  # Extract text from PDF
  pdf = fitz.open(stream=contents, filetype="pdf")
  text = ""
  for page in pdf:
    text += page.get_text()
  # Parse resume and get matching jobs
  jobs_dict = parsing.parse(index, text)
  return {"jobs": jobs_dict}
  
