# Project blueprint — RareEarthRAG

## Problem and scope
Materials researchers retrieving passages from a local paper collection. The current repository scope is described by its README and implemented files.

## Architecture and contracts
Local PDFs → page extraction → overlapping chunks → TF-IDF index → ranked source passages. User content is untrusted data. Errors should be shown without disclosing private contents.

## Ground truth and review
Outputs must be checked against the input document, audio, or user-supplied evidence. No automated score proves scientific correctness or job suitability.

## Known limits
Retrieval only: no generated answer, embeddings or vector database; no benchmark.

## Next milestone and acceptance
Synthetic/permissioned corpus, labelled relevance set, then citation-grounded answer generation. The milestone is complete only when its implementation, meaningful tests, and measured results are committed.

## Release gate
Run automated tests, inspect realistic end-to-end output, record actual failures and limitations, and update the README before claiming the milestone.
