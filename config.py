"""
config.py

Central place for file paths and settings used across the project.
Keeping this in one file makes it easy to change paths later
without hunting through every script.
"""

import os

# Base directory of the project (folder that contains this file)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data folders
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
CLEANED_DATA_DIR = os.path.join(DATA_DIR, "cleaned")
EMBEDDINGS_DIR = os.path.join(DATA_DIR, "embeddings")
SAMPLE_DATA_DIR = os.path.join(BASE_DIR, "sample_data")

# Specific files used throughout the app
RAW_COMPANIES_FILE = os.path.join(RAW_DATA_DIR, "companies_raw.json")
CLEANED_COMPANIES_FILE = os.path.join(CLEANED_DATA_DIR, "companies_cleaned.json")
SAMPLE_COMPANIES_FILE = os.path.join(SAMPLE_DATA_DIR, "companies_sample.json")

EMBEDDINGS_FILE = os.path.join(EMBEDDINGS_DIR, "company_embeddings.npy")
FAISS_INDEX_FILE = os.path.join(EMBEDDINGS_DIR, "company_index.faiss")
EMBEDDINGS_META_FILE = os.path.join(EMBEDDINGS_DIR, "embeddings_meta.json")

# Sentence Transformers model used for embeddings and search.
# This is a small, fast model that works well for short text like
# company descriptions.
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# How many results semantic search returns by default
DEFAULT_SEARCH_RESULTS = 5

# Flask settings
FLASK_DEBUG = True
FLASK_PORT = 5000
