# processing/file_loader.py
import os
import fitz  # PyMuPDF
import docx

def load_pdf(path):
    """Extract text from a PDF, keeping page numbers + filename."""
    docs = []
    filename = os.path.basename(path)
    with fitz.open(path) as pdf:
        for page_num, page in enumerate(pdf, start=1):
            text = page.get_text().strip()
            if text:  # skip empty pages
                docs.append({
                    "text": text,
                    "page": page_num,
                    "source": filename
                })
    return docs

def load_docx(path):
    """Extract text from DOCX, treat whole doc as one chunk."""
    filename = os.path.basename(path)
    doc = docx.Document(path)
    full_text = "\n".join([para.text for para in doc.paragraphs])
    return [{
        "text": full_text,
        "page": None,  # DOCX doesn’t have pages
        "source": filename
    }]

def load_txt(path):
    """Extract text from TXT, treat whole file as one chunk."""
    filename = os.path.basename(path)
    with open(path, "r", encoding="utf-8") as f:
        full_text = f.read()
    return [{
        "text": full_text,
        "page": None,
        "source": filename
    }]

def load_documents(folder):
    """Load all supported documents in folder with metadata."""
    docs = []
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if file.endswith(".pdf"):
            docs.extend(load_pdf(path))
        elif file.endswith(".docx"):
            docs.extend(load_docx(path))
        elif file.endswith(".txt"):
            docs.extend(load_txt(path))
    return docs
