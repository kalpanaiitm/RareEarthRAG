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
