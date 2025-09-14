from fastapi import FastAPI

# Create the FastAPI app
app = FastAPI()

@app.post("/upload")
def upload_file():
    return {"message": "File uploaded successfully"}

@app.get("/search")
def search_keyword(keyword: str):
    return {"Skills": ["Python", "FastAPI", "AI"]}
