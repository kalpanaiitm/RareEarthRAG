from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RareEarthSearchEngine:
    """Simple scientific literature search engine using TF-IDF."""

    def __init__(self, documents: List[Dict[str, str]]):
        self.documents = documents
        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=8000, ngram_range=(1, 2))
        self.document_vectors = None

    def build_index(self) -> None:
        """Build TF-IDF search index from document chunks."""
        texts = [doc["text"] for doc in self.documents]
        if not texts or not any(text.strip() for text in texts):
            raise ValueError("At least one non-empty passage is required.")
        self.document_vectors = self.vectorizer.fit_transform(texts)

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, str]]:
        """Search document chunks and return top matching results."""
        if self.document_vectors is None:
            raise ValueError("Index has not been built. Call build_index() first.")
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.document_vectors).flatten()
        top_indices = scores.argsort()[::-1][:max(0, top_k)]
        results = []
        for index in top_indices:
            if scores[index] <= 0:
                continue
            results.append({"source": self.documents[index]["source"], "text": self.documents[index]["text"], "score": float(scores[index])})
        return results
