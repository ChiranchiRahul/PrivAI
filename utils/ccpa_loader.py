# utils/ccpa_loader.py

import pdfplumber

def load_ccpa_chunks(pdf_path="data/ccpa.pdf", max_chunk_size=1000):
    chunks = []
    with pdfplumber.open(pdf_path) as pdf:
        full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    words = full_text.split()
    for i in range(0, len(words), max_chunk_size):
        chunk = " ".join(words[i:i + max_chunk_size])
        chunks.append(chunk)
    return chunks