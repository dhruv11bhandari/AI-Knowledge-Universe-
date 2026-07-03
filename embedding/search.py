"""
search.py

Ties together the embedding model and the FAISS index to answer
semantic search queries like "AI coding assistants" or
"companies building robotics models".

This module is imported by app.py, so the Flask app doesn't need to
know anything about FAISS directly - it just calls search_companies().
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from sentence_transformers import SentenceTransformer

import config
from scraper.utils import load_json
from embedding.faiss_index import load_faiss_index

# These are loaded once and reused for every search, instead of
# reloading the model/index on every request (that would be slow).
_model = None
_index = None
_companies = None
_meta = None


def _load_resources():
    """Load the model, FAISS index, and company data into memory once."""
    global _model, _index, _companies, _meta

    if _model is None:
        print("Loading embedding model for search...")
        _model = SentenceTransformer(config.EMBEDDING_MODEL_NAME)

    if _index is None:
        _index = load_faiss_index()

    if _companies is None:
        _companies = load_json(config.CLEANED_COMPANIES_FILE)

    if _meta is None:
        _meta = load_json(config.EMBEDDINGS_META_FILE)


def search_companies(query, top_k=config.DEFAULT_SEARCH_RESULTS):
    """
    Search for companies whose description is semantically similar to
    the query text. Returns a list of company dicts, most similar first.
    """
    _load_resources()

    if _index is None or not _companies:
        print("Search index or company data is missing. Run the pipeline first.")
        return []

    query_vector = _model.encode([query], convert_to_numpy=True).astype("float32")

    # FAISS returns distances and the positions (indices) of the
    # closest vectors. Smaller distance = more similar.
    distances, positions = _index.search(query_vector, top_k)

    results = []
    for distance, position in zip(distances[0], positions[0]):
        if position < 0 or position >= len(_companies):
            continue  # FAISS can return -1 if there aren't enough results

        company = _companies[position]
        result = dict(company)
        result["similarity_score"] = float(1 / (1 + distance))  # turn distance into a 0-1 style score
        results.append(result)

    return results


def find_similar_companies(slug, top_k=5):
    """
    Given a company's slug, find other companies with similar
    embeddings. Used on the company detail page.
    """
    _load_resources()

    target_index = None
    for i, meta_entry in enumerate(_meta):
        if meta_entry["slug"] == slug:
            target_index = i
            break

    if target_index is None or _index is None:
        return []

    embeddings = np.load(config.EMBEDDINGS_FILE).astype("float32")
    target_vector = embeddings[target_index].reshape(1, -1)

    # Ask for a few extra results since the company itself will be
    # the closest match to its own vector.
    distances, positions = _index.search(target_vector, top_k + 1)

    similar = []
    for distance, position in zip(distances[0], positions[0]):
        if position == target_index or position < 0:
            continue
        if position >= len(_companies):
            continue

        company = dict(_companies[position])
        company["similarity_score"] = float(1 / (1 + distance))
        similar.append(company)

        if len(similar) >= top_k:
            break

    return similar


if __name__ == "__main__":
    # Quick manual test: python embedding/search.py "AI coding assistants"
    import sys as _sys
    test_query = " ".join(_sys.argv[1:]) or "AI coding assistants"
    print(f"Searching for: {test_query}")
    for company in search_companies(test_query):
        print(f"- {company['name']} (score: {company['similarity_score']:.3f})")
