# RareEarthRAG

A scientific literature retrieval prototype for rare-earth materials chemistry. It extracts text from local PDFs and returns the most relevant passages for a research question using TF-IDF and cosine similarity.

> **Current status:** retrieval baseline. Despite the project name, this version does not yet generate LLM answers; the roadmap shows how it can develop into a citation-aware RAG system.

## Why this project

Rare-earth research spans synthesis, crystal structures, characterisation and luminescence. Finding comparable details across papers is slow. This project explores how transparent information retrieval can support literature review while using my PhD domain knowledge in rare-earth and solid-state chemistry.

## Features

- load permitted, text-based research PDFs from a local folder
- extract and organise paper text
- build a TF-IDF search index
- ask natural-language questions
- retrieve ranked passages with source names and similarity scores
- run locally without an API key or paid model

## Retrieval pipeline

```text
Research PDFs → text extraction → document sections → TF-IDF index
                                                    ↓
Question → query cleaning → cosine similarity → ranked source passages
```

## Example questions

- Which compounds show luminescence?
- What synthesis methods are discussed?
- Which papers mention powder XRD?
- Which rare-earth elements are present?
- What crystal structures are described?
- Which papers mention molybdoantimonites?

## Tech stack

Python · Streamlit · scikit-learn · PDF text extraction · TF-IDF · cosine similarity

## Run locally

```bash
git clone https://github.com/kalpanaiitm/RareEarthRAG.git
cd RareEarthRAG
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Place papers you are permitted to use in `data/papers/`. Do not commit copyrighted, confidential or unpublished documents.

## Limitations

- scanned PDFs require OCR
- lexical retrieval can miss conceptually similar passages with different wording
- the current version retrieves passages rather than generating answers
- retrieval quality has not yet been benchmarked

## Roadmap

- compare TF-IDF with sentence-transformer embeddings
- add a labelled retrieval evaluation set
- generate answers grounded in retrieved passages
- attach source citations to every answer
- extract compounds, synthesis conditions and luminescence data
- explore a chemistry-specific knowledge graph

## About the builder

Created by Dr Kalpana Govindarasan, a materials chemist transitioning into applied AI. This project connects rare-earth chemistry expertise with scientific information retrieval and responsible RAG development.

## Engineering evidence

See [project blueprint](PROJECT_BLUEPRINT.md), [architecture](ARCHITECTURE.md), [test report](TEST_REPORT.md) and [changelog](CHANGELOG.md) for implemented scope, verification and next milestones. These documents follow the human-controlled App Development Playbook; planned features are not represented as implemented.
