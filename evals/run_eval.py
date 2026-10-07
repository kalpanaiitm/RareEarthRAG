"""Labelled retrieval check on the built-in demo notes.

Reports hit@1, hit@3 and mean reciprocal rank (MRR) at the note level.
Run from the repository root: python -m evals.run_eval
"""
import json
from pathlib import Path

from src.pdf_loader import load_papers_from_folder
from src.search_engine import RareEarthSearchEngine
from src.utils import expand_query

ROOT = Path(__file__).resolve().parent.parent


def run(expand: bool = True) -> dict:
    cases = json.loads((ROOT / "evals" / "relevance_set.json").read_text(encoding="utf-8"))
    engine = RareEarthSearchEngine(load_papers_from_folder(ROOT / "data" / "demo_corpus"))
    engine.build_index()
    hit1 = hit3 = rr = 0.0
    misses = []
    for case in cases:
        query = expand_query(case["question"])[0] if expand else case["question"]
        sources = []
        for result in engine.search(query, top_k=10):
            if result["source"] not in sources:
                sources.append(result["source"])
        rank = sources.index(case["relevant"]) + 1 if case["relevant"] in sources else None
        hit1 += rank == 1
        hit3 += rank is not None and rank <= 3
        rr += 1 / rank if rank else 0
        if rank != 1:
            misses.append({"question": case["question"], "rank": rank})
    n = len(cases)
    return {"cases": n, "hit@1": hit1 / n, "hit@3": hit3 / n, "mrr": rr / n, "not_first": misses}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
