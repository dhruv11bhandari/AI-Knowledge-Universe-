"""
cleaner.py

Takes the raw company data and cleans it up:
- removes duplicate companies (by name)
- trims/cleans text fields
- normalizes category names so similar categories match
- makes sure every company has a tags list
- adds a URL-friendly "slug" field used for company pages

Run this file directly after scraper.py to produce
data/cleaned/companies_cleaned.json.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from scraper.utils import load_json, save_json, clean_whitespace, make_slug


# Some companies might list slightly different category names.
# This map normalizes them to a single consistent value.
CATEGORY_NORMALIZATION = {
    "llm": "Large Language Models",
    "large language model": "Large Language Models",
    "large language models": "Large Language Models",
    "coding assistant": "AI Coding Assistants",
    "ai coding assistants": "AI Coding Assistants",
    "robotics": "Robotics",
    "generative media": "Generative Media",
    "generative ai": "Generative Media",
    "ml infrastructure": "ML Infrastructure",
    "infrastructure": "ML Infrastructure",
    "ai agents": "AI Agents",
    "search & retrieval": "Search & Retrieval",
    "search and retrieval": "Search & Retrieval",
}


def normalize_category(category):
    """Map a raw category string to a consistent category name."""
    if not category:
        return "Uncategorized"

    key = category.strip().lower()
    return CATEGORY_NORMALIZATION.get(key, category.strip())


def remove_duplicates(companies):
    """Keep only one entry per company name (case-insensitive)."""
    seen_names = set()
    unique_companies = []

    for company in companies:
        name_key = company.get("name", "").strip().lower()
        if name_key and name_key not in seen_names:
            seen_names.add(name_key)
            unique_companies.append(company)

    return unique_companies


def clean_company(company):
    """Clean text fields and fill in missing fields for one company."""
    cleaned = dict(company)  # work on a copy

    cleaned["name"] = clean_whitespace(company.get("name", ""))
    cleaned["description"] = clean_whitespace(company.get("description", ""))
    cleaned["headquarters"] = clean_whitespace(company.get("headquarters", "Unknown"))
    cleaned["category"] = normalize_category(company.get("category", ""))
    cleaned["website"] = company.get("website", "").strip()
    cleaned["funding_stage"] = company.get("funding_stage", "Unknown")

    # Make sure list fields are always lists, even if missing
    cleaned["founders"] = company.get("founders") or []
    cleaned["technologies"] = company.get("technologies") or []
    cleaned["tags"] = company.get("tags") or []

    # Auto-generate a couple of tags from the category and technologies
    # so every company has at least some tags, even if the source data
    # didn't include any.
    auto_tags = {cleaned["category"].lower()}
    for tech in cleaned["technologies"]:
        auto_tags.add(tech.lower())

    combined_tags = set(tag.lower() for tag in cleaned["tags"]) | auto_tags
    cleaned["tags"] = sorted(combined_tags)

    # Slug used for company detail page URLs, e.g. /company/openai
    cleaned["slug"] = make_slug(cleaned["name"])

    return cleaned


def clean_all_companies():
    """Main entry point: load raw data, clean it, save the result."""
    raw_companies = load_json(config.RAW_COMPANIES_FILE)

    if not raw_companies:
        print("No raw data found. Run scraper/scraper.py first.")
        return []

    unique_companies = remove_duplicates(raw_companies)
    cleaned_companies = [clean_company(c) for c in unique_companies]

    save_json(cleaned_companies, config.CLEANED_COMPANIES_FILE)
    print(f"Cleaned {len(cleaned_companies)} companies.")
    print(f"Saved cleaned data to {config.CLEANED_COMPANIES_FILE}")

    return cleaned_companies


if __name__ == "__main__":
    clean_all_companies()
