import re
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.pdf_loader import load_papers_from_folder, load_pdf_bytes  # noqa: E402
from src.search_engine import RareEarthSearchEngine  # noqa: E402
from src.utils import clean_query, expand_query  # noqa: E402

DEMO_FOLDER = ROOT / "data" / "demo_corpus"
LOCAL_FOLDER = ROOT / "data" / "papers"
MAX_UPLOAD_MB = 20

EXAMPLE_QUESTIONS = [
    "Which compounds show luminescence?",
    "Which papers mention powder XRD?",
    "What synthesis methods are discussed?",
    "What is the lanthanide contraction?",
    "Which papers mention molybdoantimonites?",
    "How do white LEDs use phosphors?",
]

st.set_page_config(page_title="RareEarthRAG", page_icon="🔬", layout="wide")


@st.cache_resource(show_spinner=False)
def demo_engine():
    engine = RareEarthSearchEngine(load_papers_from_folder(DEMO_FOLDER))
    engine.build_index()
    return engine


@st.cache_resource(show_spinner=False)
def local_engine():
    documents = load_papers_from_folder(LOCAL_FOLDER) if LOCAL_FOLDER.exists() else []
    if not documents:
        return None
    engine = RareEarthSearchEngine(documents)
    engine.build_index()
    return engine


def upload_engine(files):
    """Index uploaded PDFs in memory for this session only."""
    key = tuple((f.name, f.size) for f in files)
    if st.session_state.get("upload_key") != key:
        documents, skipped = [], []
        for f in files:
            if f.size > MAX_UPLOAD_MB * 1024 * 1024:
                skipped.append(f"{f.name} (over {MAX_UPLOAD_MB} MB)")
                continue
            try:
                passages = load_pdf_bytes(f.name, f.getvalue())
            except Exception:
                passages = []
            if passages:
                documents.extend(passages)
            else:
                skipped.append(f"{f.name} (no extractable text; scanned PDFs need OCR)")
        engine = None
        if documents:
            engine = RareEarthSearchEngine(documents)
            engine.build_index()
        st.session_state.upload_key = key
        st.session_state.upload_engine = engine
        st.session_state.upload_skipped = skipped
    return st.session_state.upload_engine, st.session_state.upload_skipped


def md_escape(text):
    """Stop characters in extracted PDF text being read as Markdown or LaTeX."""
    return re.sub(r"([\\`*_{}\[\]<>()#+\-.!|~$])", r"\\\1", text)


def highlight(text, terms):
    """Escape the passage, then bold each matched word."""
    safe = md_escape(text)
    words = sorted({w for t in terms for w in t.split()}, key=len, reverse=True)
    for word in words:
        safe = re.sub(rf"(?i)\b({re.escape(word)})\b", r"**\1**", safe)
    return safe


st.title("🔬 RareEarthRAG")
st.markdown(
    "**Find the passages that answer your question across rare-earth materials papers**, "
    "with the source and page for every result so you can check it yourself."
)

with st.sidebar:
    st.header("Collection")
    options = ["Demo notes (built in)", "Upload my PDFs"]
    if local_engine() is not None:
        options.append("Local papers folder")
    mode = st.radio("Search in", options, label_visibility="collapsed")

    files = []
    if mode == "Upload my PDFs":
        files = st.file_uploader(
            "Text-based PDFs", type="pdf", accept_multiple_files=True,
            help=f"Up to {MAX_UPLOAD_MB} MB each. Processed in memory and discarded when you close the tab.",
        )
    st.divider()
    st.markdown(
        "**Privacy**\n\n"
        "- Uploads stay in this session's memory; nothing is saved or logged\n"
        "- No AI service or external API is called\n"
        "- Don't upload confidential or unpublished work to a public demo"
    )
    st.divider()
    st.caption(
        "Built by Dr Kalpana Govindarasan · PhD materials chemistry (IIT Madras) · "
        "[Source code](https://github.com/kalpanaiitm/RareEarthRAG)"
    )

if mode == "Demo notes (built in)":
    engine = demo_engine()
    st.info(
        "The demo uses six short teaching notes written for this app, not published papers, "
        "so it can run publicly without copyright issues. Upload your own PDFs from the sidebar to search real papers."
    )
elif mode == "Local papers folder":
    engine = local_engine()
else:
    if not files:
        st.warning("Upload one or more PDFs in the sidebar to start.")
        st.stop()
    engine, skipped = upload_engine(files)
    for item in skipped:
        st.warning(f"Skipped {item}")
    if engine is None:
        st.stop()

sources = sorted({d["source"] for d in engine.documents})
st.caption(f"{len(sources)} documents · {len(engine.documents)} searchable passages")

example = st.pills("Try an example", EXAMPLE_QUESTIONS, selection_mode="single") if hasattr(st, "pills") else None
with st.form("search"):
    query_text = st.text_input("Your question", value=example or "", placeholder="e.g. Which compounds show red emission?")
    col1, col2 = st.columns([3, 1])
    top_k = col1.slider("Number of results", 1, 10, 5)
    use_expansion = col2.toggle("Expand abbreviations", value=True, help="Adds e.g. 'x-ray diffraction' when you type XRD.")
    submitted = st.form_submit_button("Search", type="primary")

if submitted or example:
    query = clean_query(query_text)
    if not query:
        st.error("Please enter a question.")
        st.stop()
    search_query, added = expand_query(query) if use_expansion else (query, [])
    if added:
        st.caption("Also searched for: " + ", ".join(added))
    results = engine.search(search_query, top_k=top_k)
    if not results:
        st.warning("No passage shares any words with your question. Try different wording; this search matches words, not meaning.")
    for i, result in enumerate(results, start=1):
        where = result["source"] + (f" · page {result['page']}" if result.get("page") else "")
        with st.container(border=True):
            st.markdown(f"**{i}. {md_escape(where)}**  \nRelevance score: {result['score']:.2f}")
            st.markdown(highlight(result["text"], result["matched_terms"]))
            if result["matched_terms"]:
                st.caption("Why this result: shares " + ", ".join(f"'{t}'" for t in result["matched_terms"]))

with st.expander("How it works and its limits"):
    st.markdown(
        "1. Text is extracted from each PDF page and split into overlapping passages.\n"
        "2. Passages are indexed with TF-IDF, which weights words that are distinctive to a passage.\n"
        "3. Your question is compared with every passage by cosine similarity, and the closest are shown with their source.\n\n"
        "**Limits:** it matches words, not meaning, so different wording can be missed. Scanned PDFs need OCR first. "
        "It retrieves passages and does not yet write answers; that grounded-answer step is the next milestone."
    )
