import io
import re
from pathlib import Path
from typing import BinaryIO, Dict, List, Union

from pypdf import PdfReader

PAGE_MARKER = re.compile(r"--- Page (\d+) ---")


def _read_pdf_pages(source: Union[str, Path, BinaryIO]) -> List[str]:
    """Return the text of each page; empty pages are kept so page numbers stay correct."""
    reader = PdfReader(source)
    return [page.extract_text() or "" for page in reader.pages]


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from a PDF file, with a marker before each page."""
    text_parts = []
    try:
        for page_number, page_text in enumerate(_read_pdf_pages(str(pdf_path)), start=1):
            if page_text.strip():
                text_parts.append(f"\n--- Page {page_number} ---\n{page_text}")
    except Exception as error:
        print(f"Could not read {pdf_path.name}: {error}")
    return "\n".join(text_parts)


def split_text_into_chunks(text: str, chunk_size: int = 1200, overlap: int = 200) -> List[str]:
    """Split long text into overlapping chunks for search."""
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Expected chunk_size > overlap >= 0.")
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        if end >= len(text):
            break
        start = end - overlap
    return chunks


def chunk_pages(source: str, pages: List[str], chunk_size: int = 1200, overlap: int = 200) -> List[Dict]:
    """Chunk each page separately so every passage carries its page number."""
    documents = []
    for page_number, page_text in enumerate(pages, start=1):
        for chunk in split_text_into_chunks(page_text, chunk_size, overlap):
            documents.append({"source": source, "page": page_number, "text": chunk})
    return documents


def load_pdf_bytes(name: str, data: bytes) -> List[Dict]:
    """Load an uploaded PDF held in memory. Nothing is written to disk."""
    return chunk_pages(name, _read_pdf_pages(io.BytesIO(data)))


def load_text_file(path: Path) -> List[Dict]:
    """Load a Markdown or text note, splitting on blank lines into paragraph passages."""
    text = path.read_text(encoding="utf-8")
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    title = paragraphs[0].lstrip("# ").strip() if paragraphs else path.stem
    documents = []
    for paragraph in paragraphs[1:]:
        if paragraph.startswith("Written for the RareEarthRAG demo"):
            continue
        documents.append({"source": title, "page": None, "text": paragraph})
    return documents


def load_papers_from_folder(folder_path: Path) -> List[Dict]:
    """Load all PDFs (and .md/.txt notes) from a folder and return searchable passages."""
    documents = []
    for pdf_file in sorted(folder_path.glob("*.pdf")):
        try:
            documents.extend(chunk_pages(pdf_file.name, _read_pdf_pages(str(pdf_file))))
        except Exception as error:
            print(f"Could not read {pdf_file.name}: {error}")
    for note in sorted(list(folder_path.glob("*.md")) + list(folder_path.glob("*.txt"))):
        if note.name.lower() == "readme.md":
            continue
        documents.extend(load_text_file(note))
    return documents
