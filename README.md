# Smart Resume Search API

A **FastAPI-based application** to upload, parse, and query resumes in PDF format.  
Supports single and multi-keyword searches and returns structured JSON highlighting **Skills**, **Experience**, and **Projects**. Optional support for non-resume PDFs is also included.

---

## Executive Summary / Key Innovations
- Fast, vector-based search using **FAISS** for scalable queries.
- Supports **multi-keyword search** across multiple PDFs.
- Handles PDFs without predefined sections, returning generic content if needed.
- Recruiter-friendly structured output for resumes.
- Modular architecture, easy to extend for future improvements.

---

## Features
- Upload multiple PDFs at once.
- Query resumes using single or multiple keywords.
- Extract structured information (**Skills**, **Experience**, **Projects**) from PDFs.
- Supports PDFs without predefined sections (returns content in a generic **Content** field).
- Fast vector-based search using **FAISS**.
- Ready for recruiter-friendly output.

---

## System Architecture
+----------------+ +----------------+ +-----------------+ +------------------+
| PDF Upload | ---> | PDF Parsing & | ---> | FAISS Vector | ---> | Query API / JSON |
| (POST /upload)| | Embeddings | | Store | | Response |
+----------------+ +----------------+ +-----------------+ +------------------+

yaml
Copy code

---

## Folder Structure
smart_resume_search/
├── app/
│ ├── main.py # FastAPI app
│ ├── utils.py # Helper functions
│ ├── models.py # Model loading & embeddings
├── uploaded_pdfs/ # Uploaded PDF storage
├── tests/ # Unit and integration tests
├── docs/ # Architecture diagrams, guides
├── requirements.txt # Python dependencies
├── README.md
└── .gitignore

yaml
Copy code

---

## Developer Guide

### Run the FastAPI Server
```bash
uvicorn app.main:app --reload
Access API Documentation
Swagger UI: http://127.0.0.1:8000/docs

Redoc: http://127.0.0.1:8000/redoc

Run Tests & Check Coverage
bash
Copy code
pytest tests/               # Run all tests
pytest --cov=app tests/     # Check test coverage
User Guide
Upload PDFs
Endpoint: POST /upload_pdfs
Description: Upload one or multiple PDF resumes.

Request Example (cURL):

bash
Copy code
curl -X POST "http://127.0.0.1:8000/upload_pdfs" \
  -F "files=@Resume1.pdf" \
  -F "files=@Resume2.pdf"
Response Example:

json
Copy code
{
  "status": "uploaded",
  "files": ["Resume1.pdf", "Resume2.pdf"]
}
Single Keyword Search
Endpoint: POST /query_resume
Description: Search for a single keyword across all uploaded PDFs.

Request Example:

json
Copy code
{
  "keyword": "Computer Vision"
}
Response Example:

json
Copy code
{
  "Resume1.pdf": {
    "Skills": ["Computer Vision", "Python"],
    "Experience": ["Worked on Computer Vision project for object detection."],
    "Projects": ["Project1: Computer Vision E-commerce application"]
  }
}
Multi-Keyword Search
Endpoint: POST /multi_search
Description: Search using multiple keywords across all uploaded PDFs.

Request Example:

json
Copy code
{
  "keywords": ["React", "Machine Learning"]
}
Response Example:

json
Copy code
{
  "Resume1.pdf": {
    "Skills": ["React", "Python", "Machine Learning"],
    "Projects": ["Project2: React Dashboard"]
  },
  "Resume2.pdf": {
    "Skills": ["React", "Machine Learning"]
  }
}
List Uploaded PDFs
Endpoint: GET /list_files
Description: List all PDFs uploaded to the system.

Response Example:

json
Copy code
{
  "uploaded_files": ["Resume1.pdf", "Resume2.pdf"]
}
Performance & Limitations
FAISS vector search ensures fast keyword lookups, even with dozens of PDFs.

Handles PDFs with non-standard formats, but extremely large PDFs may take longer to process.

Designed for local infrastructure and free/open-source tools.

Contributing
Open issues or submit pull requests for bug fixes, improvements, or new features.

License
MIT License