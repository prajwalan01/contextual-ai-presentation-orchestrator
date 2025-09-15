from fastapi import FastAPI, UploadFile, File, Query
from typing import List
import pdfplumber
import re

app = FastAPI(title="Smart Resume Search API")

resumes = []
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB per file

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Smart Resume Search API is live! Visit /docs for Swagger UI."}

# Upload PDFs
@app.post("/upload_pdfs")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    """
    Upload multiple PDF resumes.
    Rejects files larger than MAX_FILE_SIZE (5 MB).
    Parses PDF text and stores in memory.
    """
    global resumes
    resumes = []
    for file in files:
        # Check file size
        file.file.seek(0, 2)  # move to end
        size = file.file.tell()
        file.file.seek(0)  # reset pointer
        if size > MAX_FILE_SIZE:
            return {"error": f"{file.filename} is too large. Max 5 MB allowed."}

        text = ""
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "

        # Normalize text: lowercase, remove extra spaces/newlines
        text = re.sub(r"\s+", " ", text.lower()).strip()
        
        # Optional debug: print first 500 chars
        print(f"Extracted from {file.filename}:\n{text[:500]}")
        
        resumes.append({"name": file.filename, "text": text})
    
    return {"message": f"{len(resumes)} resumes uploaded successfully"}

# Search resumes by query parameter
@app.get("/search")
async def search(query: str = Query(..., description="Keyword or multi-word query")):
    """
    Search resumes by keyword or multi-word query.
    Returns resumes containing the query with a text snippet.
    """
    query = query.lower().strip()
    results = []
    pattern = re.compile(re.escape(query))
    for resume in resumes:
        if pattern.search(resume['text']):
            results.append({
                "name": resume['name'],
                "text_snippet": resume['text'][:200]
            })
    return {"query": query, "results": results}

# Clear uploads
@app.post("/clear_uploads")
async def clear_uploads():
    """
    Clear all previously uploaded resumes.
    """
    global resumes
    resumes = []
    return {"message": "All uploads cleared"}
