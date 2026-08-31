import fitz
from docx import Document


def extract_text(path):
    if path.lower().endswith('.pdf'):
        doc = fitz.open(path)
        return "\n".join(page.get_text() for page in doc)
    if path.lower().endswith('.docx'):
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError("Only PDF and DOCX files are supported.")
