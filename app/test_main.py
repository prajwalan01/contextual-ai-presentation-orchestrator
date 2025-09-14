from .main import app  # Relative import avoids circular import
from fastapi.testclient import TestClient
from fpdf import FPDF
import os

client = TestClient(app)

# Auto-generate a minimal sample PDF if it doesn't exist
PDF_FILE = "sample_resume.pdf"
if not os.path.exists(PDF_FILE):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Name: John Doe", ln=True)
    pdf.cell(200, 10, txt="Skills: Python, FastAPI, AI", ln=True)
    pdf.output(PDF_FILE)

def test_upload_pdf():
    with open(PDF_FILE, "rb") as f:
        response = client.post("/upload", files={"file": (PDF_FILE, f, "application/pdf")})
    assert response.status_code == 200
    assert "uploaded successfully" in response.text

def test_search_keyword():
    response = client.get("/search?keyword=Python")
    assert response.status_code == 200
    data = response.json()
    assert "Skills" in data
    assert isinstance(data["Skills"], list)
