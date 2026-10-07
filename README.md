# RareEarthRAG

**Find the passages that answer your question across rare-earth materials papers, with the source and page for every result.**

[**Try the live demo →**](https://rareearthrag-capbrkuce3iesfc6zngwrl.streamlit.app/) · No sign-up · No API key · Uploaded PDFs are not stored

---

## The problem

A literature review in rare-earth materials chemistry means reading dozens of papers to answer narrow questions: *Which compounds show red Eu³⁺ emission? Who used hydrothermal synthesis? Which papers report powder XRD and Rietveld refinement?* The answers are buried in methods and results sections, spread across many PDFs, and a normal PDF search only finds exact phrases in one file at a time.

General AI chatbots can summarise papers, but they may state things the papers never said, and it is hard to check where an answer came from. In research, an answer you cannot trace to a page is not much use.

## What RareEarthRAG does

- **Searches many papers at once.** Ask a question in plain English and get the most relevant passages from all loaded papers, ranked.
- **Shows where every result comes from:** the file name and page number, so you can go straight to the source.
- **Explains why a passage was chosen** by highlighting the words it shares with your question.
- **Understands common abbreviations** in the field. A search for *XRD* also searches for *x-ray diffraction*, *PL* for *photoluminescence*, and so on.
- **Never invents text.** Every result is a passage copied from a paper. Nothing is generated.

It is built by a materials chemist (PhD on rare-earth molybdoantimonites, IIT Madras; postdoc, University of Southampton) as a first step towards a citation-grounded research assistant.

## Who it is for

- Postgraduate students and researchers starting a literature review in rare-earth or luminescent materials
- Anyone who needs to compare synthesis or characterisation details across several papers
- Teachers preparing material on lanthanide chemistry

## Privacy

Research papers can be unpublished or confidential, so the app is designed to keep them private:

| | |
| --- | --- |
| **Uploaded PDFs** | Read in memory for your session only. They are never written to disk, saved to a database or logged, and they are discarded when you close the tab. |
| **Your questions** | Not stored or sent anywhere. |
| **Third-party AI** | None. All searching happens inside the app with scikit-learn; no text is sent to OpenAI or any other AI service. |
| **Accounts and tracking** | No sign-up. The app adds no analytics of its own and turns off Streamlit's usage statistics. |
| **Hosting** | The public demo runs on Streamlit Community Cloud, which keeps standard server logs. For confidential work, run the app on your own computer (below); then nothing leaves your machine. |

Please do not upload confidential or unpublished documents to the public demo. Only upload papers you have the right to use.

## The demo collection

The public demo includes six short **teaching notes written for this app**: lanthanide luminescence, synthesis routes, characterisation methods, the lanthanide contraction, molybdate and antimonite hosts, and applications and supply. They are clearly labelled as notes, not published papers, so the demo can run publicly without copyright problems. To search real papers, upload them in the app or run it locally.

## Example questions

- Which compounds show luminescence?
- Which papers mention powder XRD?
- What synthesis methods are discussed?
- What is the lanthanide contraction?
- Which papers mention molybdoantimonites?
- How do white LEDs use phosphors?

## How it works

```text
PDFs ─► text extracted page by page ─► overlapping passages (page number kept)
                                                │
                                                ▼
Question ─► abbreviation expansion ─► TF-IDF ─► cosine similarity ─► ranked passages
                                                                      + source, page, matched words
```

TF-IDF gives extra weight to words that are distinctive to a passage, such as *molybdate* or *Rietveld*, and less to common words. Cosine similarity then measures how closely each passage matches the question.

## Evaluation

`evals/relevance_set.json` holds 15 questions, each labelled with the demo note that should answer it. Run `python -m evals.run_eval` to get hit@1, hit@3 and mean reciprocal rank.

Current result: **15/15 questions return the correct note first.** This is a sanity check rather than a benchmark: the same person wrote the questions and the notes, so the wording overlaps more than it would with real papers. A harder test on real, permitted papers is on the roadmap.

## Run it on your own computer

```bash
git clone https://github.com/kalpanaiitm/RareEarthRAG.git
cd RareEarthRAG
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

To search a fixed set of papers, put the PDFs in `data/papers/`. They appear in the app as **Local papers folder**. This folder is excluded from Git so papers are never committed by accident.

Run the tests with `pip install -r requirements-dev.txt` and then `python -m pytest -q`.

## Limitations

- It matches **words, not meaning**: a passage that says *emits red light* may be missed by a search for *luminescence*.
- Scanned PDFs have no text layer and need OCR first; the app tells you when a file is skipped.
- It retrieves passages and does **not** yet write answers.
- Tables, equations and figure contents are often extracted poorly from PDFs.

## Roadmap

- [x] Built-in demo collection, PDF upload and page-level sources
- [x] Labelled retrieval check with hit@k and MRR
- [ ] Compare TF-IDF with sentence-transformer embeddings for meaning-based search
- [ ] Generate short answers from the retrieved passages, with a citation for every sentence
- [ ] Extract compounds, synthesis conditions and emission wavelengths into a table
- [ ] Evaluate on a set of open-access papers

## Tech stack

Python · Streamlit · scikit-learn (TF-IDF, cosine similarity) · pypdf

## About the builder

Created by **Dr Kalpana Govindarasan**, a materials chemist moving into applied AI. More projects: [github.com/kalpanaiitm](https://github.com/kalpanaiitm)

See the [project blueprint](PROJECT_BLUEPRINT.md), [architecture](ARCHITECTURE.md), [test report](TEST_REPORT.md) and [changelog](CHANGELOG.md) for implemented scope and next steps. Planned features are not presented as implemented.
