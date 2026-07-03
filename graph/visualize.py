"""
visualize.py

Turns the NetworkX knowledge graph into an interactive HTML graph
using PyVis. The generated HTML is saved into static/ so Flask can
serve it directly and embed it in an iframe on the graph page.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyvis.network import Network

import config
from graph.graph_builder import build_knowledge_graph

# Colors for each category, so the graph is easier to read at a glance.
CATEGORY_COLORS = {
    "Large Language Models": "#6C5CE7",
    "AI Coding Assistants": "#00B894",
    "Robotics": "#E17055",
    "Generative Media": "#0984E3",
    "ML Infrastructure": "#FDCB6E",
    "AI Agents": "#E84393",
    "Search & Retrieval": "#00CEC9",
    "Uncategorized": "#B2BEC3",
}

GRAPH_OUTPUT_PATH = os.path.join(config.BASE_DIR, "static", "graph.html")


def build_and_save_graph_html(highlight_slug=None):
    """
    Build the knowledge graph and save it as an interactive HTML file
    at static/graph.html. If highlight_slug is given, that node is
    drawn larger/highlighted (used on company detail pages).
    """
    graph = build_knowledge_graph()

    network = Network(
        height="600px",
        width="100%",
        bgcolor="#111111",
        font_color="white",
        notebook=False,
    )

    # Add nodes with category-based colors
    for node_id, node_data in graph.nodes(data=True):
        category = node_data.get("category", "Uncategorized")
        color = CATEGORY_COLORS.get(category, "#B2BEC3")
        size = 30 if node_id == highlight_slug else 18

        network.add_node(
            node_id,
            label=node_data.get("name", node_id),
            title=f"{node_data.get('name')} ({category})",
            color=color,
            size=size,
        )

    # Add edges, using the stored reasons as the hover tooltip
    for source, target, edge_data in graph.edges(data=True):
        reasons = ", ".join(edge_data.get("reasons", []))
        network.add_edge(source, target, title=reasons)

    # Nice default physics settings so the graph doesn't jitter forever
    network.set_options("""
    {
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -8000,
          "springLength": 120
        },
        "minVelocity": 0.75
      }
    }
    """)

    os.makedirs(os.path.dirname(GRAPH_OUTPUT_PATH), exist_ok=True)
    network.write_html(GRAPH_OUTPUT_PATH)
    print(f"Saved interactive graph to {GRAPH_OUTPUT_PATH}")

    return GRAPH_OUTPUT_PATH


if __name__ == "__main__":
    build_and_save_graph_html()
