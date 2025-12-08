from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import fitz  # pymupdf
from Helper_Scripts import parsing
import json
import threading
import time
import traceback

# Import scraper function from Scraping.remote_scraper
try:
    from Scraping.remote_scraper import scraper as run_remote_scraper
except Exception:
    # If import fails, set to None and continue; app will still run
    run_remote_scraper = None
    print("Warning: could not import Scraping.remote_scraper.scraper")
    traceback.print_exc()


app = FastAPI()


# Enable CORS for all origins (development only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/tags")
async def get_tags():
    """Return canonical tag filters defined in the backend parsing module."""
    try:
        tags = getattr(parsing, "TAG_FILTERS", [])
    except Exception:
        tags = []
    return {"tags": tags}


def _scraper_loop(interval_seconds: int = 24 * 3600):
    if run_remote_scraper is None:
        print("Remote scraper unavailable; background scraper will not run.")
        return

    while True:
        try:
            print("[scraper loop] Starting remote scraper run...")
            run_remote_scraper()
            print("[scraper loop] Remote scraper finished.")
        except Exception as e:
            print("[scraper loop] Error running remote scraper:", e)
            traceback.print_exc()

        # Sleep for the configured interval
        time.sleep(interval_seconds)


@app.on_event("startup")
def start_background_scraper():
    """Start scraper thread on application startup. Runs immediately, then every 24h."""
    if run_remote_scraper is None:
        print("Skipping background scraper startup: scraper not available.")
        return

    thread = threading.Thread(target=_scraper_loop, name="background-scraper", daemon=True)
    thread.start()
    print("Background scraper thread started (runs every 24h).")
  
