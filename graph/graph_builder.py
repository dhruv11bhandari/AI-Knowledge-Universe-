"""
graph_builder.py

Builds a knowledge graph where each node is a company and edges connect
companies that are related in some way:

- same category
- shared founder
- shared technology
- high embedding similarity

Each edge stores a "reason" so the UI can explain *why* two companies
are connected, instead of just showing a line between them.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import networkx as nx

import config
from scraper.utils import load_json

# Companies need at least this much cosine similarity to be linked
# purely based on their embeddings (separate from shared category/tech).
EMBEDDING_SIMILARITY_THRESHOLD = 0.6


def cosine_similarity(vec_a, vec_b):
    """Standard cosine similarity between two vectors."""
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))


def add_edge_with_reason(graph, company_a, company_b, reason):
    """
    Add an edge between two companies. If an edge already exists,
    just append the new reason instead of overwriting it, so a pair
    of companies can be connected for more than one reason.
    """
    slug_a = company_a["slug"]
    slug_b = company_b["slug"]

    if graph.has_edge(slug_a, slug_b):
        existing_reasons = graph[slug_a][slug_b]["reasons"]
        if reason not in existing_reasons:
            existing_reasons.append(reason)
    else:
        graph.add_edge(slug_a, slug_b, reasons=[reason])


def build_knowledge_graph():
    """
    Build the full knowledge graph from cleaned company data and
    (if available) their embeddings.
    """
    companies = load_json(config.CLEANED_COMPANIES_FILE)
    if not companies:
        print("No cleaned data found. Run scraper/cleaner.py first.")
        return nx.Graph()

    graph = nx.Graph()

    # Add one node per company, storing a few useful fields on the node
    # itself so the frontend doesn't need a separate lookup.
    for company in companies:
        graph.add_node(
            company["slug"],
            name=company["name"],
            category=company["category"],
            description=company["description"],
        )

    # --- Connect companies that share a category ---
    for i, company_a in enumerate(companies):
        for company_b in companies[i + 1:]:
            if company_a["category"] == company_b["category"]:
                add_edge_with_reason(graph, company_a, company_b, "same category")

    # --- Connect companies that share a founder ---
    for i, company_a in enumerate(companies):
        founders_a = set(f.lower() for f in company_a.get("founders", []))
        for company_b in companies[i + 1:]:
            founders_b = set(f.lower() for f in company_b.get("founders", []))
            if founders_a & founders_b:  # any overlap
                add_edge_with_reason(graph, company_a, company_b, "shared founder")

    # --- Connect companies that share a technology ---
    for i, company_a in enumerate(companies):
        tech_a = set(t.lower() for t in company_a.get("technologies", []))
        for company_b in companies[i + 1:]:
            tech_b = set(t.lower() for t in company_b.get("technologies", []))
            if tech_a & tech_b:
                add_edge_with_reason(graph, company_a, company_b, "shared technology")

    # --- Connect companies with similar embeddings, if embeddings exist ---
    if os.path.exists(config.EMBEDDINGS_FILE) and os.path.exists(config.EMBEDDINGS_META_FILE):
        embeddings = np.load(config.EMBEDDINGS_FILE)
        meta = load_json(config.EMBEDDINGS_META_FILE)

        for i in range(len(meta)):
            for j in range(i + 1, len(meta)):
                similarity = cosine_similarity(embeddings[i], embeddings[j])
                if similarity >= EMBEDDING_SIMILARITY_THRESHOLD:
                    company_a = next(c for c in companies if c["slug"] == meta[i]["slug"])
                    company_b = next(c for c in companies if c["slug"] == meta[j]["slug"])
                    add_edge_with_reason(graph, company_a, company_b, "similar description")

    print(f"Built graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges.")
    return graph


if __name__ == "__main__":
    build_knowledge_graph()
