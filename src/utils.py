import re


def clean_query(query: str) -> str:
    """Clean a user query before search."""
    if not query:
        return ""
    query = query.strip()
    query = re.sub(r"\s+", " ", query)
    return query
