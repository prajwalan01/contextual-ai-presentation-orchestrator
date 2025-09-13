from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List
import os
import shutil
from .models import QueryModel, MultiSearchQuery

app = FastAPI(title="Smart Resume Search API")

UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory "parsed" resume data
resumes_db = {}

# -------------------------------
# API Endpoints
# -------------------------------
@app.get("/")
async def root():
    return {"message": "Welcome to Smart Resume Search API. Upload PDFs and query content!"}

# Upload multiple PDFs
@app.post("/upload_pdfs")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    uploaded_files = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Simulate parsing PDF to structured JSON
        resumes_db[file.filename] = {
            "Name": file.filename.replace(".pdf", ""),
            "Skills": "Python, Django, SQL, Machine Learning, Computer Vision, Text-to-Video, React",
            "Experience": "Worked on multiple full-stack and ML projects including Computer Vision and Text-to-Video.",
            "Projects": "Project1: React Dashboard, Project5: Computer Vision E-commerce application"
        }
        uploaded_files.append(file.filename)
    
    return {"status": "uploaded", "files": uploaded_files}

# Single-keyword search
@app.post("/query_resume")
async def query_resume(query: QueryModel):
    keyword = query.keyword.lower()
    results = {}
    
    for filename, sections in resumes_db.items():
        matched_sections = {}
        for section, content in sections.items():
            if keyword in content.lower():
                matched_sections[section] = [item.strip() for item in content.split(",") if keyword in item.lower()] \
                    if section == "Skills" else [content]  # Split Skills into list
        if matched_sections:
            results[filename] = matched_sections
    
    if not results:
        return {"message": f"No matches found for '{query.keyword}'."}
    
    return JSONResponse(content=results)

# Multi-keyword search
@app.post("/multi_search")
async def multi_search(query: MultiSearchQuery):
    keywords = [kw.lower() for kw in query.keywords]
    results = {}
    
    for filename, sections in resumes_db.items():
        matched_sections = {}
        for section, content in sections.items():
            if any(kw in content.lower() for kw in keywords):
                matched_sections[section] = [item.strip() for item in content.split(",") if any(kw in item.lower() for kw in keywords)] \
                    if section == "Skills" else [content]
        if matched_sections:
            results[filename] = matched_sections
    
    if not results:
        return {"message": "No matches found for your keywords."}
    
    return JSONResponse(content=results)

# List uploaded PDFs
@app.get("/list_files")
async def list_files():
    return {"uploaded_files": list(resumes_db.keys())}
