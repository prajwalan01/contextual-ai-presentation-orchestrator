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
- Deployed on **Render** for instant access.

---

## Deployment

- **Render URL:** [https://smart-resume-search.onrender.com](https://smart-resume-search.onrender.com)  
- **Swagger UI:** [https://smart-resume-search.onrender.com/docs](https://smart-resume-search.onrender.com/docs)  

---

## How to Run Locally

1. Clone the repository:  
```bash
git clone https://github.com/your-username/smart-resume-search.git
cd smart-resume-search
Create and activate a virtual environment:

python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt


Start the FastAPI server:

uvicorn main:app --reload


Open Swagger UI at: http://127.0.0.1:8000/docs

How to Use (Demo Flow)
1. Upload PDFs

Go to /upload endpoint in Swagger UI.

Upload one or multiple resumes.

Example Response:

{
  "message": "2 PDFs uploaded successfully."
}

2. Search by Keyword

Go to /search endpoint.

Enter a single keyword (e.g., "python") and click Execute.

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

Currently only one keyword per request is supported.

Run searches sequentially for multiple keywords (e.g., "python", "AI", "FastAPI") to get full results.

Notes / Limitations

Multiple keywords in a single request are not supported (workaround: sequential searches).

Free-tier Render has limited storage and memory.

Previous uploads are cleared on every new upload.

For large-scale or production use, consider paid hosting or local hosting.

Project Structure
smart-resume-search/
│
├─ main.py          # FastAPI application
├─ requirements.txt # Dependencies
├─ uploads/         # Folder for uploaded PDFs (auto-cleared)
├─ README.md        # This file
└─ .venv/           # Virtual environment (optional)

Demo Tips

Pre-upload PDFs before starting the demo.

Use the Swagger UI /search endpoint for interactive testing.

For multiple keywords, run one query at a time.

Keep JSON responses visible for clarity during presentations.

Author

Prajwal Andure
AI & Computer Vision Developer
