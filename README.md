# Smart Resume Search API

A **FastAPI-based application** to upload, parse, and search resumes in PDF format.  
Supports **single-keyword searches** and returns structured JSON highlighting **Skills**, **Experience**, and **Projects**.

---

## Key Features

- Upload **multiple PDF resumes** at once.  
- Automatically clears previous uploads on each new upload.  
- Search resumes for a **single keyword**.  
- Returns results in structured JSON.  
- Swagger UI available for **interactive API testing**.

---

## How to Run

### 1. Run Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --reload
Open Swagger UI: http://127.0.0.1:8000/docs

2. Using Render Deployment

Deployment link: https://smart-resume-search.onrender.com

Swagger UI: https://smart-resume-search.onrender.com/docs
How to Use (Demo Flow)

Upload PDFs

Use the /upload endpoint in Swagger UI.

Upload one or multiple resumes.

Search by Keyword

Use the /search endpoint.

Enter a single keyword (e.g., "python").

Get results in JSON format.

Repeat Search for Multiple Keywords

Currently, only single keyword per request is supported.

For multiple keywords, run multiple searches sequentially.

Example Usage
1. Upload PDFs

Endpoint: /upload

Method: POST

Example Response:

{
  "message": "2 PDFs uploaded successfully."
}
2. Search by Keyword

Endpoint: /search

Method: POST

Example Request:

{
  "query": "python"
}


Example Response:

{
  "query": "python",
  "results": [
    {
      "filename": "resume1.pdf",
      "matches": ["Python Developer", "Python, Django, FastAPI"]
    },
    {
      "filename": "resume2.pdf",
      "matches": ["Python, AI Projects"]
    }
  ]
}
3. Multiple Keywords Workaround

Currently only one keyword per request.

Run searches sequentially for multiple keywords (e.g., "python", "AI", "FastAPI") to get full results.

Notes / Limitations

Multiple keywords in one request not supported (workaround: search sequentially).

Storage and memory are limited on free-tier Render.

The app deletes previous uploads on new upload.

For large-scale or production use, consider paid hosting or local hosting.
Project Structure
smart-resume-search/
│
├─ main.py          # FastAPI application
├─ requirements.txt # Dependencies
├─ uploads/         # Folder where uploaded PDFs are stored (auto-cleared)
├─ README.md        # This file
└─ .venv/           # Virtual environment (optional)
## Demo Tips

- Pre-upload PDFs before starting your demo.  
- Use Swagger UI `/search` endpoint for interactive demo.  
- For multiple keywords, run one query at a time to avoid redeployment.  
- Keep JSON response visible for clarity.
