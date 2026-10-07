import re
from typing import List, Tuple

# Common abbreviations in rare-earth materials papers. TF-IDF only matches exact
# words, so a query for "XRD" would otherwise miss "X-ray diffraction".
ABBREVIATIONS = {
    "xrd": "x-ray diffraction",
    "pxrd": "powder x-ray diffraction",
    "pl": "photoluminescence",
    "ple": "photoluminescence excitation",
    "sem": "scanning electron microscopy",
    "edx": "energy-dispersive x-ray spectroscopy",
    "tga": "thermogravimetric analysis",
    "led": "light-emitting diode",
    "ree": "rare-earth elements",
    "cie": "chromaticity coordinates",
}


def clean_query(query: str) -> str:
    """Clean a user query before search."""
    if not query:
        return ""
    query = query.strip()
    query = re.sub(r"\s+", " ", query)
    return query


def expand_query(query: str) -> Tuple[str, List[str]]:
    """Add the long form of known abbreviations; return the query and what was added."""
    words = re.findall(r"[a-z0-9]+", query.lower())
    added = [ABBREVIATIONS[w] for w in dict.fromkeys(words) if w in ABBREVIATIONS]
    expanded = " ".join([query] + added) if added else query
    return expanded, added
