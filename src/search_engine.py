from typing import Dict, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RareEarthSearchEngine:
    """Simple scientific literature search engine using TF-IDF."""

    def __init__(self, documents: List[Dict]):
        self.documents = documents
        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=8000, ngram_range=(1, 2))
        self.document_vectors = None

    def build_index(self) -> None:
        """Build TF-IDF search index from document chunks."""
        texts = [doc["text"] for doc in self.documents]
        if not texts or not any(text.strip() for text in texts):
            raise ValueError("At least one non-empty passage is required.")
        self.document_vectors = self.vectorizer.fit_transform(texts)

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search document chunks and return top matching results.

        Each result includes the terms shared by the query and the passage,
        so a reader can see why it was ranked.
        """
        if self.document_vectors is None:
            raise ValueError("Index has not been built. Call build_index() first.")
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.document_vectors).flatten()
        top_indices = scores.argsort()[::-1][:max(0, top_k)]
        vocabulary = self.vectorizer.get_feature_names_out()
        query_terms = set(query_vector.indices)
        results = []
        for index in top_indices:
            if scores[index] <= 0:
                continue
            row = self.document_vectors[index]
            shared = sorted(query_terms.intersection(row.indices))
            document = self.documents[index]
            results.append({
                "source": document["source"],
                "page": document.get("page"),
                "text": document["text"],
                "score": float(scores[index]),
                "matched_terms": [str(vocabulary[i]) for i in shared],
            })
        return results
