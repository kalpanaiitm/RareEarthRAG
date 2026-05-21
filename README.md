# RareEarthRAG

A beginner-friendly Scientific AI project for searching and summarising rare-earth materials research papers.

This project is designed as a portfolio project for a Materials Chemistry / Rare Earth Chemistry background transitioning into Agentic AI, Retrieval-Augmented Generation (RAG), and Materials Informatics.

## What this project does

RareEarthRAG lets you:

- Add rare-earth chemistry PDF papers
- Extract text from PDFs
- Search across papers using similarity search
- Ask questions such as:
  - Which compounds show luminescence?
  - What synthesis methods were used?
  - Which papers mention powder XRD?
  - What rare-earth elements are discussed?
- View the most relevant text snippets from the paper collection

This first version uses **TF-IDF similarity search** so it can run without paid APIs or advanced setup.

## Why this project matters

Rare-earth materials are important in luminescence, solid-state chemistry, phosphors, magnets, energy materials, and advanced functional materials.

This project demonstrates how AI and information retrieval can support scientific literature review and materials discovery.

## Skills demonstrated

- Python
- Scientific text processing
- PDF text extraction
- TF-IDF similarity search
- Materials Informatics
- Rare-earth chemistry domain knowledge
- Streamlit app development
- Foundation for RAG systems

## Folder structure

```text
RareEarthRAG/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── papers/
├── src/
│   ├── pdf_loader.py
│   ├── search_engine.py
│   └── utils.py
└── examples/
    └── sample_questions.md
```

## How to run locally

```bash
git clone https://github.com/YOURUSERNAME/RareEarthRAG.git
cd RareEarthRAG
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

For Mac/Linux, use:

```bash
source venv/bin/activate
```

## Add PDFs

Put PDF research papers inside:

```text
data/papers/
```

## Example questions

- Which papers mention rare earth molybdoantimonites?
- What synthesis methods are discussed?
- Which compounds show luminescence?
- What characterisation techniques are used?
- Which papers mention powder XRD?
- Which rare-earth elements are present?

## Future improvements

- Add sentence-transformer embeddings
- Add LLM summarisation
- Add citation-aware answers
- Add compound extraction
- Add rare-earth element tagging
- Add chemistry-specific knowledge graph
- Add comparison tables for synthesis, structure, and luminescence data

## Author positioning

Created by a PhD Materials Chemist with rare-earth and solid-state chemistry research experience, building AI tools for scientific knowledge retrieval and materials informatics.
