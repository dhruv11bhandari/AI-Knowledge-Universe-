"""
utils.py

Small helper functions used by the scraper and cleaner scripts.
Nothing fancy here, just reusable bits of logic.
"""

import json
import os
import re


def load_json(file_path):
    """Load a JSON file and return its contents. Returns an empty list
    if the file does not exist yet (useful the first time you run things)."""
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, file_path):
    """Save data to a JSON file, creating the parent folder if needed."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def clean_whitespace(text):
    """Collapse multiple spaces/newlines into a single space and trim."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def make_slug(name):
    """Turn a company name into a URL-friendly slug, e.g. 'OpenAI' -> 'openai'."""
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug
