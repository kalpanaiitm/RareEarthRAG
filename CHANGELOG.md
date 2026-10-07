# Changelog

## 2026-10-07 — Public demo
- Built-in demo collection of six labelled teaching notes, so the hosted app works without copyrighted papers.
- In-memory PDF upload (20 MB limit), skipped-file messages for scanned PDFs, and an optional local papers folder.
- Page numbers kept for every passage; matched words highlighted with a "why this result" line.
- Abbreviation expansion for common characterisation terms (XRD, PL, SEM, ...).
- Labelled relevance set (15 questions) with hit@1, hit@3 and MRR in `evals/run_eval.py`.
- README rewritten: problem, audience, privacy, evaluation and limits. Streamlit usage statistics turned off.

## 2026-09-28 — Portfolio review
Documented the current architecture and explicit limits following the App Development Playbook. Next milestone: Synthetic/permissioned corpus, labelled relevance set, then citation-grounded answer generation.
