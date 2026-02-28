import os
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

def extract_from_pdf(path: str) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(path)
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return "\n".join(text)

def extract_from_html(url: str) -> str:
    """Extract visible text from a webpage."""
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove scripts and styles
    for tag in soup(["script", "style"]):
        tag.decompose()

    return soup.get_text(separator="\n", strip=True)

def extract_from_txt(path: str) -> str:
    """Extract text from a plain text file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_text(source: str) -> str:
    """
    Determine the type of document and extract text accordingly.
    - If source starts with http, treat as URL.
    - If source ends with .pdf, treat as PDF.
    - If source ends with .txt, treat as text file.
    """
    if source.startswith("http://") or source.startswith("https://"):
        return extract_from_html(source)

    ext = os.path.splitext(source)[1].lower()

    if ext == ".pdf":
        return extract_from_pdf(source)
    elif ext == ".txt":
        return extract_from_txt(source)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
