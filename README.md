# Smart Resume Search API

A **FastAPI-based application** to upload, parse, and query resumes in PDF format.  
Supports single and multi-keyword searches and returns structured JSON highlighting **Skills**, **Experience**, and **Projects**. Optional support for non-resume PDFs is also included.

---

## Key Features

- Upload multiple PDF resumes at once.
- Automatically clears previous uploads on each new upload to ensure only current PDFs are searchable.
- Single and multi-keyword search across all uploaded PDFs.
- Lists uploaded PDFs.

---

## Workflow

```text
+----------------+       +----------------+       +-----------------+       +------------------+
| PDF Ingestion  |  -->  | Embedding      |  -->  | Vector Database |  -->  | Query Interface  |
| & Preprocessing|       | Generation     |       | (FAISS)         |       | (FastAPI/Swagger)|
+----------------+       +----------------+       +-----------------+       +------------------+
PDF Ingestion: Upload and parse PDFs, extract text. Previous uploads are cleared automatically.

Embedding Generation: Convert text chunks into vector embeddings.

Vector Database (FAISS): Store embeddings for fast similarity search.

Query Interface: Accept keyword queries, return structured JSON results.

Folder Structure
text
Copy code
smart_resume_search/
├── app/
│   ├── main.py        # FastAPI app
│   ├── utils.py       # Helper functions
│   ├── models.py      # Model loading & embeddings
├── uploaded_pdfs/     # Uploaded PDF storage (cleared on new upload)
├── tests/             # Unit and integration tests
├── docs/              # Architecture diagrams, guides
├── requirements.txt   # Python dependencies
├── README.md
└── .gitignore
Developer Guide
Run the FastAPI Server
uvicorn app.main:app --reload
Access API Documentation:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

Run Tests
pytest tests/               # Run all tests
pytest --cov=app tests/     # Check test coverage
User Guide
Upload PDFs
Endpoint: POST /upload_pdfs
Description: Upload one or multiple PDF resumes. Previous uploads are cleared automatically.

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

{
  "keyword": "Python"
}
Response Example:

json
Copy code
{
  "Resume1.pdf": {
    "Skills": ["Python"],
    "Experience": [],
    "Projects": []
  }
}
Multi-Keyword Search
Endpoint: POST /multi_search
Description: Search using multiple keywords across all uploaded PDFs.

Request Example:

json
Copy code
{
  "keywords": ["Python", "React"]
}
Response Example:

json
Copy code
{
  "Resume1.pdf": {
    "Skills": ["Python", "React"],
    "Experience": [],
    "Projects": []
  }
}
List Uploaded PDFs
Endpoint: GET /list_files
Description: List all PDFs currently uploaded to the system.

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

Previous uploads are automatically cleared on new uploads to prevent old PDFs from appearing in search results.

Contributing
Open issues or submit pull requests for bug fixes, improvements, or new features.

License
MIT License

🚀 Live Demo
The project is deployed and accessible at:

Live App: https://contextual-ai-presentation-orchestrator-2.onrender.com

Swagger UI (API docs): https://contextual-ai-presentation-orchestrator-2.onrender.com/docs

ReDoc (alt docs): https://contextual-ai-presentation-orchestrator-2.onrender.com/redoc

yaml
Copy code
