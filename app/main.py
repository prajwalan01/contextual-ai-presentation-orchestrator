from fastapi import FastAPI, UploadFile, File
import os
from fpdf import FPDF
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss

app = FastAPI(title="Contextual AI Presentation Orchestrator")

# Directory for uploaded PDFs
UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Dummy sentence-transformer + FAISS setup (for demonstration)
model = SentenceTransformer('all-MiniLM-L6-v2')
dimension = 384  # embedding dimension for this model
index = faiss.IndexFlatL2(dimension)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload PDF files."""
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Optional: generate a dummy PDF for testing if needed
    if file.filename == "sample_resume.pdf" and os.path.getsize(file_path) == 0:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Name: John Doe", ln=True)
        pdf.cell(200, 10, txt="Skills: Python, FastAPI, AI", ln=True)
        pdf.output(file_path)

    return {"message": f"{file.filename} uploaded successfully"}


@app.get("/search")
async def search_keyword(keyword: str):
    """Dummy search endpoint returning skills for demonstration."""
    # In real scenario, you can extract text from PDFs and perform vector search
    if keyword.lower() == "python":
        return {"Skills": ["Python", "FastAPI", "AI"]}
    else:
        return {"Skills": []}


# Railway deployment: run with uvicorn
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Railway sets PORT automatically
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
