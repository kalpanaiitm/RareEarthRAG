from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from a PDF file."""
    text_parts = []
    try:
        reader = PdfReader(str(pdf_path))
        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""
            if page_text.strip():
                text_parts.append(f"\n--- Page {page_number} ---\n{page_text}")
    except Exception as error:
        print(f"Could not read {pdf_path.name}: {error}")
    return "\n".join(text_parts)


def split_text_into_chunks(text: str, chunk_size: int = 1200, overlap: int = 200) -> List[str]:
    """Split long text into overlapping chunks for search."""
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start = end - overlap
    return chunks


def load_papers_from_folder(folder_path: Path) -> List[Dict[str, str]]:
    """Load all PDF papers from a folder and return searchable text chunks."""
    documents = []
    pdf_files = list(folder_path.glob("*.pdf"))
    for pdf_file in pdf_files:
        full_text = extract_text_from_pdf(pdf_file)
        chunks = split_text_into_chunks(full_text)
        for chunk in chunks:
            documents.append({"source": pdf_file.name, "text": chunk})
    return documents
