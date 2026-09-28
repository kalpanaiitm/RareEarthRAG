# Architecture

Local PDFs → page extraction → overlapping chunks → TF-IDF index → ranked source passages.

The README names the runnable entry point. Components should keep validation separate from the core operation and presentation. The existing code is the source of truth; this page does not claim planned capabilities as implemented.

## Failure and privacy boundaries
Retrieval only: no generated answer, embeddings or vector database; no benchmark. Use non-sensitive or permitted inputs for demos. Do not commit user documents, audio, credentials, or generated outputs.
