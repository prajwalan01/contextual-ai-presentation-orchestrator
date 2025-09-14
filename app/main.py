from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
from typing import List
import shutil
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os

app = FastAPI(title="Contextual AI Presentation Orchestrator")

UPLOAD_FOLDER = Path(__file__).parent.parent / "uploaded_pdfs"
UPLOAD_FOLDER.mkdir(exist_ok=True)

# Initialize model
model = SentenceTransformer("all-MiniLM-L6-v2")

# In-memory FAISS index
faiss_index = None
file_mapping = []


def clear_previous_uploads():
    """Clear previously uploaded PDFs."""
    for f in UPLOAD_FOLDER.iterdir():
        if f.is_file() and f.suffix.lower() == ".pdf":
            f.unlink()


def extract_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def build_index():
    global faiss_index, file_mapping
    faiss_index = None
    file_mapping = []

    all_texts = []
    for pdf_file in UPLOAD_FOLDER.iterdir():
        if pdf_file.suffix.lower() != ".pdf":
            continue
        text = extract_text(pdf_file)
        if text.strip() == "":
            continue
        all_texts.append((pdf_file.name, text))

    if not all_texts:
        return

    texts = [txt for _, txt in all_texts]
    embeddings = model.encode(texts, convert_to_numpy=True)
    faiss_index = faiss.IndexFlatL2(embeddings.shape[1])
    faiss_index.add(embeddings)
    file_mapping = [fname for fname, _ in all_texts]


@app.post("/upload_pdfs")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    clear_previous_uploads()  # Remove old PDFs

    saved_files = []
    for file in files:
        save_path = UPLOAD_FOLDER / file.filename
        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file.filename)

    build_index()
    return {"status": "uploaded", "files": saved_files}


@app.post("/query_resume")
async def query_resume(keyword: str):
    if faiss_index is None or not file_mapping:
        return JSONResponse(content={"message": "No PDFs uploaded"}, status_code=400)

    query_vec = model.encode([keyword], convert_to_numpy=True)
    D, I = faiss_index.search(query_vec, k=len(file_mapping))

    result = {}
    for idx in I[0]:
        fname = file_mapping[idx]
        result[fname] = {"Skills": [keyword]}  # Simplified for demo
    return result


@app.get("/list_files")
async def list_files():
    files = [f.name for f in UPLOAD_FOLDER.iterdir() if f.is_file() and f.suffix.lower() == ".pdf"]
    return {"uploaded_files": files}
