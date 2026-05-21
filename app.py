import streamlit as st
from pathlib import Path

from src.pdf_loader import load_papers_from_folder
from src.search_engine import RareEarthSearchEngine
from src.utils import clean_query

st.set_page_config(page_title="RareEarthRAG", page_icon="🔬", layout="wide")

st.title("🔬 RareEarthRAG")
st.subheader("Rare-Earth Materials Literature Search Assistant")

st.write("""
This app searches rare-earth materials chemistry papers using PDF text extraction
and TF-IDF similarity search. It is a beginner-friendly foundation for a future
RAG system.
""")

papers_folder = Path("data/papers")

with st.sidebar:
    st.header("Project Info")
    st.write("**Domain:** Rare Earth Materials")
    st.write("**Techniques:** PDF extraction, TF-IDF, similarity search")
    st.write("**AI Direction:** Materials Informatics + RAG")
    st.divider()
    st.write("Add PDF papers to:")
    st.code("data/papers/")

papers_folder.mkdir(parents=True, exist_ok=True)
documents = load_papers_from_folder(papers_folder)

if len(documents) == 0:
    st.warning("No PDF papers found. Please add PDFs to the data/papers folder.")
    st.stop()

st.success(f"Loaded {len(documents)} paper text sections.")

search_engine = RareEarthSearchEngine(documents)
search_engine.build_index()

st.header("Ask a question about your rare-earth papers")

default_questions = [
    "Which compounds show luminescence?",
    "What synthesis methods are discussed?",
    "Which papers mention powder XRD?",
    "Which rare-earth elements are present?",
    "What crystal structures are described?",
    "Which papers mention molybdoantimonites?"
]

selected_question = st.selectbox("Choose an example question or type your own below:", [""] + default_questions)
user_query = st.text_input("Your question:", value=selected_question, placeholder="Example: Which compounds show luminescence?")
top_k = st.slider("Number of results", min_value=1, max_value=10, value=5)

if st.button("Search Papers"):
    query = clean_query(user_query)
    if not query:
        st.error("Please enter a question.")
    else:
        results = search_engine.search(query, top_k=top_k)
        st.subheader("Most relevant results")
        for i, result in enumerate(results, start=1):
            with st.expander(f"Result {i}: {result['source']} | Score: {result['score']:.3f}"):
                st.write(result["text"])

st.divider()
st.caption("RareEarthRAG — Scientific AI portfolio project for Materials Informatics.")
