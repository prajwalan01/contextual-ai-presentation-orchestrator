from fastapi import FastAPI, UploadFile, File, Form
from typing import List, Dict
import pdfplumber
import re

app = FastAPI(title="Smart Resume Search API")

# In-memory storage for uploaded resumes
resumes = []

# -----------------------
# Upload PDFs Endpoint
# -----------------------
@app.post("/upload_pdfs")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    """
    Upload multiple PDF resumes.
    Clears previous uploads automatically.
    """
    global resumes
    resumes = []  # Clear previous uploads
    for file in files:
        text = ""
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
        # Normalize text: lowercase, remove extra spaces/newlines
        text = re.sub(r"\s+", " ", text.lower()).strip()
        resumes.append({
            "name": file.filename,
            "text": text
        })
    return {"message": f"{len(resumes)} resumes uploaded successfully"}

# -----------------------
# Search Endpoint
# -----------------------
@app.get("/search")
async def search(query: str = Form(...)):
    """
    Search uploaded resumes by keyword or phrase.
    Returns resumes matching the query.
    """
    query = query.lower().strip()
    results = []

    # Regex for exact phrase matching
    pattern = re.compile(re.escape(query))

    for resume in resumes:
        if pattern.search(resume['text']):
            results.append({
                "name": resume['name'],
                "text_snippet": resume['text'][:200]  # First 200 chars as snippet
            })

    return {"query": query, "results": results}

# -----------------------
# Clear Uploads Endpoint
# -----------------------
@app.post("/clear_uploads")
async def clear_uploads():
    """
    Clear all previously uploaded PDFs.
    """
    global resumes
    resumes = []
    return {"message": "All uploads cleared"}
