# AI Knowledge Universe

An interactive web app for exploring the AI company ecosystem using semantic
search, sentence embeddings, and knowledge graphs. Built as a learning
project to practice combining a Flask backend with modern NLP tooling
(Sentence Transformers + FAISS) and graph visualization (NetworkX + PyVis).

## Project Overview

AI Knowledge Universe lets you:

- Search for AI companies using natural language (e.g. *"companies building
  robotics models"*) instead of exact keyword matches
- Browse a dashboard with stats and category breakdowns
- View a company's profile, including related and semantically similar
  companies
- Explore an interactive knowledge graph showing how companies connect
  through shared categories, founders, technologies, and description
  similarity

The dataset ships with 20 curated AI companies (`sample_data/`) so the whole
pipeline runs out of the box without needing to scrape the web.

## Features

- **Data pipeline** — cleans and normalizes company data (dedupe, tag
  generation, category normalization)
- **Semantic search** — Sentence Transformer embeddings + a FAISS index for
  fast nearest-neighbor search
- **Knowledge graph** — a NetworkX graph connecting companies by shared
  category, founder, technology, or embedding similarity, rendered as an
  interactive PyVis graph
- **Company pages** — overview, technologies, related companies (graph
  neighbors), and similar companies (embedding neighbors)
- **Dashboard** — total companies, category counts, recent additions, and a
  search box

## Technologies Used

| Layer          | Tools                                             |
|----------------|----------------------------------------------------|
| Backend        | Python, Flask                                     |
| NLP / Search   | Sentence Transformers, FAISS                      |
| Data           | BeautifulSoup, requests, JSON/CSV                 |
| Graph          | NetworkX, PyVis                                   |
| Visualization  | Plotly, PyVis                                     |
| Frontend       | HTML, CSS, JavaScript (no framework)              |

## Project Structure

```
project/
├── app.py                  # Flask app + routes
├── config.py                # Shared paths and settings
├── requirements.txt
│
├── data/
│   ├── raw/                 # Raw company data (generated)
│   ├── cleaned/              # Cleaned company data (generated)
│   └── embeddings/          # Saved vectors + FAISS index (generated)
│
├── scraper/
│   ├── scraper.py           # Collects raw data (sample dataset by default)
│   ├── cleaner.py           # Dedupe, clean text, normalize categories, tags
│   └── utils.py
│
├── embedding/
│   ├── embed.py             # Generates Sentence Transformer embeddings
│   ├── faiss_index.py       # Builds/loads the FAISS index
│   └── search.py            # Semantic search + "similar companies"
│
├── graph/
│   ├── graph_builder.py     # Builds the NetworkX knowledge graph
│   └── visualize.py         # Renders the graph with PyVis
│
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── images/
│
├── templates/
│   ├── base.html
│   ├── index.html           # Dashboard
│   ├── search.html
│   ├── company.html
│   └── graph.html
│
└── sample_data/
    └── companies_sample.json
```

## Installation

1. **Clone the repo and create a virtual environment**

   ```bash
   git clone <your-repo-url>
   cd project
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the data pipeline** (only needs to be done once, or whenever the
   sample dataset changes)

   ```bash
   python scraper/scraper.py      # copies sample data into data/raw/
   python scraper/cleaner.py      # cleans it into data/cleaned/
   python embedding/embed.py      # generates embeddings
   python embedding/faiss_index.py  # builds the FAISS index
   python graph/visualize.py      # pre-builds the graph HTML (optional, app can do this on demand)
   ```

4. **Run the app**

   ```bash
   python app.py
   ```

   Then open `http://localhost:5000` in your browser.

> Note: the first time you run `embed.py`, Sentence Transformers will
> download the `all-MiniLM-L6-v2` model (a few hundred MB). This requires
> an internet connection but only happens once — it's cached locally after
> that.

## Screenshots

*(Add screenshots of the dashboard, search results, company page, and graph
view here once you've run the app locally.)*

## Future Improvements

- Replace the sample dataset with a real scraper for specific AI company
  directories
- Add a proper database (SQLite or Postgres) instead of JSON files
- Add pagination and filters to the search results page
- Cache the knowledge graph instead of rebuilding it on every request to
  `/graph`
- Add unit tests for the cleaning and graph-building logic
- Deploy the app (e.g. Render, Railway, or Heroku) with a persistent
  embeddings index

## License

This is a student portfolio project, free to use and adapt for learning
purposes.


python3 -m venv venv
source venv/bin/activate
python scraper/scraper.py
python scraper/cleaner.py
python embedding/embed.py
python embedding/faiss_index.py
