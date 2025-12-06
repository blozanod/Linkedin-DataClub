from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()




@app.get("/")
async def root():
  return {"message": "Hello"}

app.post("/get_jobs")
async def root():
  return {"message": "Here are the jobs"}

# Point of communcation between:
# 1. Helper Functions
# 2. Frontend