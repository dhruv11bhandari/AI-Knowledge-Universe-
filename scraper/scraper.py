"""
scraper.py

Collects raw company data for the project.

For this student project we mostly rely on a curated sample dataset
(sample_data/companies_sample.json) instead of scraping many different
company websites, since every company has a different page layout and
a "real" scraper would need a custom parser per site.

We do include one small example function, scrape_company_page(), that
shows how you *would* pull a short description off a public webpage
using requests + BeautifulSoup, in case you want to extend this later.

Run this file directly to copy the sample dataset into data/raw/,
which is the starting point for the rest of the pipeline.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from bs4 import BeautifulSoup

import config
from scraper.utils import load_json, save_json, clean_whitespace


def scrape_company_page(url):
    """
    Example of a simple scraper for a single webpage.

    This grabs the page title and the first paragraph of text as a
    rough "description". Real company sites vary a lot, so this is
    meant as a starting point, not a complete solution.
    """
    headers = {"User-Agent": "Mozilla/5.0 (AI Knowledge Universe student project)"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as error:
        print(f"Could not fetch {url}: {error}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string if soup.title else ""
    first_paragraph = soup.find("p")
    description = clean_whitespace(first_paragraph.get_text()) if first_paragraph else ""

    return {
        "name": clean_whitespace(title),
        "description": description,
        "website": url,
    }


def load_sample_dataset():
    """Load the curated sample companies that ship with this project."""
    return load_json(config.SAMPLE_COMPANIES_FILE)


def collect_raw_data():
    """
    Main entry point for data collection.

    Loads the sample dataset and writes it to data/raw/companies_raw.json.
    This keeps the rest of the pipeline (cleaning, embeddings, etc.)
    working the same way whether the data came from scraping or from
    a curated list.
    """
    companies = load_sample_dataset()
    print(f"Loaded {len(companies)} companies from sample dataset.")

    save_json(companies, config.RAW_COMPANIES_FILE)
    print(f"Saved raw data to {config.RAW_COMPANIES_FILE}")

    return companies


if __name__ == "__main__":
    collect_raw_data()
