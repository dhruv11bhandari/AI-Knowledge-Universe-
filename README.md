<div align="center">

# AI Knowledge Universe

### *Explore the AI Ecosystem through Semantic Search, Knowledge Graphs & Modern NLP*

<img src="https://readme-typing-svg.demolab.com?font=Poppins&weight=600&size=28&pause=1200&color=00C2FF&center=true&vCenter=true&width=900&lines=Semantic+Search+Powered+by+Sentence+Transformers;Knowledge+Graphs+with+NetworkX+%26+PyVis;Natural+Language+Company+Discovery;Built+with+Flask+%7C+FAISS+%7C+Python" />

<br>

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_App-black?style=for-the-badge&logo=flask)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-red?style=for-the-badge)
![Sentence Transformers](https://img.shields.io/badge/Sentence_Transformers-NLP-success?style=for-the-badge)
![NetworkX](https://img.shields.io/badge/Knowledge_Graph-NetworkX-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

---

### Discover AI companies using **Natural Language Search** instead of traditional keyword matching.

</div>

---

# Overview

AI Knowledge Universe is an interactive AI exploration platform that combines **semantic search**, **vector embeddings**, and **knowledge graphs** into one intuitive web application.

Instead of searching for exact company names, users can ask questions naturally:

> *"Companies building robotics foundation models"*

The system understands the **meaning** of your query using Sentence Transformers, finds the most relevant companies with **FAISS**, and visualizes relationships through an interactive **knowledge graph**.

This project was built to learn how modern AI applications combine NLP, graph analytics, and web development into a single intelligent system.

---

# Features

## Semantic AI Search

- Natural language company search
- Sentence Transformer embeddings
- Fast FAISS similarity search
- Finds relevant companies even without keyword matches

---

## Interactive Knowledge Graph

Visualize how AI companies connect through:

- Shared technologies
- Common founders
- Similar industries
- Semantic similarity
- Categories

Built using **NetworkX + PyVis**.

---

## Dashboard

View:

- Company statistics
- Category distribution
- Recent additions
- Quick semantic search
- Interactive company explorer

---

## Company Profiles

Every company includes:

- Description
- Technologies
- Categories
- Related companies
- Similar companies using embeddings

---

## Data Pipeline

Automatic preprocessing includes:

- Data cleaning
- Deduplication
- Category normalization
- Tag generation
- Embedding generation
- FAISS index creation

---

# Architecture

```text
                 Raw Company Data
                        │
                        ▼
               Data Cleaning Pipeline
                        │
                        ▼
           Sentence Transformer Embeddings
                        │
                        ▼
               FAISS Vector Index
                        │
                        ▼
          Semantic Search Engine
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
Knowledge Graph                  Flask Dashboard
(NetworkX + PyVis)             Search + Company Pages
```

---

# Tech Stack

| Layer | Technologies |
|--------|--------------|
| Backend | Flask, Python |
| NLP | Sentence Transformers |
| Vector Search | FAISS |
| Graph Analytics | NetworkX |
| Graph Visualization | PyVis |
| Data Processing | BeautifulSoup, Requests |
| Visualization | Plotly |
| Frontend | HTML, CSS, JavaScript |

---

# Project Structure

```text
project/
│
├── app.py
├── config.py
├── requirements.txt
│
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── embeddings/
│
├── scraper/
│   ├── scraper.py
│   ├── cleaner.py
│   └── utils.py
│
├── embedding/
│   ├── embed.py
│   ├── faiss_index.py
│   └── search.py
│
├── graph/
│   ├── graph_builder.py
│   └── visualize.py
│
├── static/
├── templates/
└── sample_data/
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/yourusername/AI-Knowledge-Universe.git

cd AI-Knowledge-Universe
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Data Pipeline

```bash
python scraper/scraper.py

python scraper/cleaner.py

python embedding/embed.py

python embedding/faiss_index.py

python graph/visualize.py
```

---

# Launch the Application

```bash
python app.py
```

Visit

```
http://localhost:5000
```

---

#  Screenshots

## Dashboard

<p align="center">
<img src="https://github.com/user-attachments/assets/aaca6534-a2f2-4f8b-8142-55514519e4ff" width="900">
</p>

---

## Knowledge Graph

<p align="center">
<img src="https://github.com/user-attachments/assets/5462768f-d958-4877-848e-b6525b821cd6" width="900">
</p>

---

#  Future Roadmap

- Real AI company scraper
- SQLite/PostgreSQL integration
- Graph filtering
- Advanced semantic filters
- User authentication
- Company comparison
- AI-powered recommendations
- Cached graph generation
- Docker deployment
- Cloud deployment

---

#  Learning Outcomes

This project demonstrates practical experience with:

Semantic Search

Vector Databases

Sentence Embeddings

FAISS

Knowledge Graphs

Flask Development

Data Engineering

NLP Pipelines

---

# Contributing

Contributions are always welcome.

If you'd like to improve the project:

- Fork the repository
- Create a feature branch
- Commit your changes
- Submit a Pull Request

---

# License

Released under the MIT License.

Feel free to use this project for learning, experimentation, and educational purposes.

---

<div align="center">

### ⭐ If you found this project interesting, consider giving it a star!

Made with ❤️ by **Dhruv Bhandari**

</div>
