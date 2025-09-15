from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
import shutil

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = FastAPI()

# Lazy-loaded model (simulate heavy load)
model = None
def load_model():
    global model
    if model is None:
        print("Loading model...")
        # Replace with your actual ML model if needed
        import time
        time.sleep(2)
        model = "Model ready"
    return model

# Utility to clear old files
def clear_uploads():
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

@app.post("/upload/")
async def upload_files(files: list[UploadFile] = File(...)):
    clear_uploads()  # delete old PDFs
    saved_files = []
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        saved_files.append(file.filename)
    return {"uploaded_files": saved_files}

@app.get("/search/")
def search(query: str):
    load_model()  # lazy-load model
    # For demo, just search file names
    results = [f for f in os.listdir(UPLOAD_FOLDER) if query.lower() in f.lower()]
    return JSONResponse({"query": query, "results": results})

@app.get("/")
def root():
    return {"message": "PDF Search API is live"}
