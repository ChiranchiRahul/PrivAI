# utils/dpdpa_loader.py

import pdfplumber
import os

def load_dpdpa_chunks(pdf_path="data/dpdpa_2023.pdf", chunk_size=800):
    """Reads DPDPA PDF and splits into clean text chunks."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"DPDPA PDF not found at: {pdf_path}")
    
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"

    # Clean up and chunk the text
    cleaned = text.replace("\n", " ").strip()
    chunks = [cleaned[i:i + chunk_size] for i in range(0, len(cleaned), chunk_size)]
    return chunks
