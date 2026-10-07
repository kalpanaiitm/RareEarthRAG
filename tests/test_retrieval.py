import pytest
from src.pdf_loader import split_text_into_chunks
from src.search_engine import RareEarthSearchEngine

def test_chunker_terminates_and_validates_overlap():
    assert split_text_into_chunks("abc", chunk_size=10, overlap=2) == ["abc"]
    with pytest.raises(ValueError):
        split_text_into_chunks("abc", chunk_size=2, overlap=2)

def test_retrieval_returns_only_positive_matches():
    engine = RareEarthSearchEngine([{"source": "a.pdf", "text": "Powder diffraction of crystals"}])
    engine.build_index()
    assert engine.search("diffraction")[0]["source"] == "a.pdf"
    assert engine.search("unrelatedword") == []


def test_engine_explains_matches_and_keeps_page():
    engine = RareEarthSearchEngine([
        {"source": "a.pdf", "page": 3, "text": "Eu3+ red emission in a molybdate host"},
        {"source": "b.pdf", "page": 1, "text": "Hydrothermal synthesis in an autoclave"},
    ])
    engine.build_index()
    top = engine.search("red emission")[0]
    assert top["page"] == 3
    assert "emission" in top["matched_terms"]


def test_expand_query_adds_long_forms_once():
    from src.utils import expand_query
    expanded, added = expand_query("XRD and xrd patterns")
    assert added == ["x-ray diffraction"]
    assert expanded.endswith("x-ray diffraction")
    assert expand_query("lanthanide contraction") == ("lanthanide contraction", [])


def test_demo_corpus_loads_with_titles_and_no_disclaimer_passages():
    from pathlib import Path
    from src.pdf_loader import load_papers_from_folder
    docs = load_papers_from_folder(Path(__file__).resolve().parent.parent / "data" / "demo_corpus")
    assert len({d["source"] for d in docs}) == 6
    assert all(d["source"].startswith("Demo note") for d in docs)
    assert not any(d["text"].startswith("Written for") for d in docs)


def test_uploaded_pdf_keeps_page_numbers():
    import io
    from reportlab.pdfgen import canvas
    from src.pdf_loader import load_pdf_bytes
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(72, 700, "first page")
    pdf.showPage()
    pdf.drawString(72, 700, "powder diffraction on page two")
    pdf.save()
    docs = load_pdf_bytes("t.pdf", buffer.getvalue())
    assert [d["page"] for d in docs] == [1, 2]


def test_labelled_demo_set_ranks_expected_note_in_top_three():
    from evals.run_eval import run
    assert run()["hit@3"] >= 0.9
