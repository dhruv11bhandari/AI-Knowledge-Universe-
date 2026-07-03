"""
app.py

Main Flask application for AI Knowledge Universe.

Routes:
- /                 dashboard with stats + search box
- /search           semantic search results page
- /company/<slug>   individual company page
- /graph            full interactive knowledge graph

Run with: python app.py
Make sure you've run the data pipeline first (see README.md).
"""

from flask import Flask, render_template, request
from collections import Counter
import os

import config
from scraper.utils import load_json
from embedding.search import search_companies, find_similar_companies
from graph.graph_builder import build_knowledge_graph
from graph.visualize import build_and_save_graph_html, GRAPH_OUTPUT_PATH

app = Flask(__name__)


def get_all_companies():
    """Load the cleaned company dataset used by most pages."""
    return load_json(config.CLEANED_COMPANIES_FILE)


def get_company_by_slug(slug):
    """Find one company by its slug, or None if it doesn't exist."""
    for company in get_all_companies():
        if company["slug"] == slug:
            return company
    return None


@app.route("/")
def dashboard():
    """Dashboard: total companies, category breakdown, recent additions."""
    companies = get_all_companies()

    category_counts = Counter(c["category"] for c in companies)

    # "Recent" additions: since we don't have real timestamps in this
    # student project, we just show the last few entries in the dataset.
    recent_companies = companies[-5:][::-1]

    return render_template(
        "index.html",
        total_companies=len(companies),
        category_counts=category_counts.most_common(),
        recent_companies=recent_companies,
    )


@app.route("/search")
def search():
    """Semantic search page. Query comes from ?q=... in the URL."""
    query = request.args.get("q", "").strip()
    results = search_companies(query) if query else []

    return render_template("search.html", query=query, results=results)


@app.route("/company/<slug>")
def company_page(slug):
    """Individual company page with related + similar companies."""
    company = get_company_by_slug(slug)
    if company is None:
        return render_template("company.html", company=None, slug=slug), 404

    # "Similar companies" = closest embeddings (semantic similarity)
    similar_companies = find_similar_companies(slug, top_k=5)

    # "Related companies" = directly connected in the knowledge graph
    # (same category, shared founder, shared technology, etc.)
    graph = build_knowledge_graph()
    related_companies = []
    if slug in graph:
        for neighbor_slug in graph.neighbors(slug):
            neighbor_company = get_company_by_slug(neighbor_slug)
            if neighbor_company:
                reasons = graph[slug][neighbor_slug]["reasons"]
                related_companies.append({"company": neighbor_company, "reasons": reasons})

    return render_template(
        "company.html",
        company=company,
        similar_companies=similar_companies,
        related_companies=related_companies,
    )


@app.route("/graph")
def graph_page():
    """Full interactive knowledge graph page."""
    # Rebuild the graph HTML on demand. For a small dataset like this
    # it's fast enough to do on every visit; a bigger project would
    # cache this instead.
    if not os.path.exists(GRAPH_OUTPUT_PATH):
        build_and_save_graph_html()

    return render_template("graph.html")


if __name__ == "__main__":
    app.run(debug=config.FLASK_DEBUG, port=config.FLASK_PORT)
