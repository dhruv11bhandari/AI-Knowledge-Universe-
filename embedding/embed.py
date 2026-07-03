"""
embed.py

Generates a sentence embedding (a vector of numbers) for each company's
description using Sentence Transformers. These vectors are what let us
do semantic search later, since similar meanings end up close together
in vector space even if the exact words are different.

Run this file after scraper/cleaner.py to produce:
- data/embeddings/company_embeddings.npy   (the vectors)
- data/embeddings/embeddings_meta.json     (company names/slugs, same order as vectors)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from sentence_transformers import SentenceTransformer

import config
from scraper.utils import load_json, save_json


def build_text_for_embedding(company):
    """
    Combine a company's description with its category and technologies
    into one piece of text. This gives the embedding model more context
    than the description alone, which usually improves search quality.
    """
    parts = [
        company.get("description", ""),
        "Category: " + company.get("category", ""),
        "Technologies: " + ", ".join(company.get("technologies", [])),
    ]
    return ". ".join(part for part in parts if part.strip())


def generate_embeddings():
    """Load cleaned companies, embed them, and save the vectors + metadata."""
    companies = load_json(config.CLEANED_COMPANIES_FILE)

    if not companies:
        print("No cleaned data found. Run scraper/cleaner.py first.")
        return

    print(f"Loading embedding model: {config.EMBEDDING_MODEL_NAME}")
    model = SentenceTransformer(config.EMBEDDING_MODEL_NAME)

    texts = [build_text_for_embedding(c) for c in companies]

    print(f"Generating embeddings for {len(texts)} companies...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    os.makedirs(config.EMBEDDINGS_DIR, exist_ok=True)
    np.save(config.EMBEDDINGS_FILE, embeddings)

    # Save metadata (name + slug) in the same order as the embeddings,
    # so we can map a vector back to a company later.
    meta = [{"name": c["name"], "slug": c["slug"]} for c in companies]
    save_json(meta, config.EMBEDDINGS_META_FILE)

    print(f"Saved embeddings to {config.EMBEDDINGS_FILE}")
    print(f"Saved embedding metadata to {config.EMBEDDINGS_META_FILE}")


if __name__ == "__main__":
    generate_embeddings()
