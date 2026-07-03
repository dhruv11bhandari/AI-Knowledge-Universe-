"""
faiss_index.py

Builds a FAISS index from the embeddings we generated in embed.py.
FAISS lets us search for the "nearest" vectors to a query vector very
quickly, which is how semantic search finds the most similar companies.

We use a simple flat L2 index here. It's not the fastest option for
huge datasets, but for a project with a few hundred companies it's
plenty fast and easy to understand.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import faiss

import config


def build_faiss_index():
    """Build a FAISS index from the saved embeddings and save it to disk."""
    if not os.path.exists(config.EMBEDDINGS_FILE):
        print("No embeddings found. Run embedding/embed.py first.")
        return None

    embeddings = np.load(config.EMBEDDINGS_FILE).astype("float32")
    vector_size = embeddings.shape[1]

    # IndexFlatL2 does an exact nearest-neighbor search using
    # Euclidean (L2) distance. Simple and good enough for this project.
    index = faiss.IndexFlatL2(vector_size)
    index.add(embeddings)

    faiss.write_index(index, config.FAISS_INDEX_FILE)
    print(f"Built FAISS index with {index.ntotal} vectors.")
    print(f"Saved index to {config.FAISS_INDEX_FILE}")

    return index


def load_faiss_index():
    """Load a previously built FAISS index from disk."""
    if not os.path.exists(config.FAISS_INDEX_FILE):
        return None
    return faiss.read_index(config.FAISS_INDEX_FILE)


if __name__ == "__main__":
    build_faiss_index()
