# Test report

## Scope
This report distinguishes automated tests from an end-to-end or deployed demonstration. A passing unit test does not prove model quality, document fidelity, or deployment reliability.

## Current verification
See the tests and workflow (if present) in this repository. Local run on 2026-09-28: `python -m pytest -q` → **2 passed in 1.42s**. This is a local unit/component result; a deployed end-to-end check has not been performed.

## Update 2026-10-07
- 7 automated tests (chunking, ranking, matched-term explanations, page numbers for uploaded PDFs, demo loading, abbreviation expansion, labelled set).
- Labelled demo set: 15/15 hit@1, MRR 1.00. Questions and notes share an author, so this is a sanity check, not a benchmark.
- App smoke-tested in demo, upload (including a text-free PDF), empty-upload and no-match states. Not yet checked on the hosted deployment.

## Remaining evaluation
Synthetic/permissioned corpus, labelled relevance set, then citation-grounded answer generation.
