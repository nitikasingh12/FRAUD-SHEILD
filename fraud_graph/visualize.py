import os
from pyvis.network import Network
from graph_engine import build_graph

BASE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(os.path.dirname(BASE), "static", "fraud_network.html")

COLORS = {"phone": "#1a4d8f", "upi": "#e07b39", "account": "#2e9e5b", "device": "#8a3ffc"}


def generate_visualization():
    G = build_graph()
    net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="#14213d")
    net.barnes_hut(gravity=-3000, spring_length=120)

    degrees = dict(G.degree())
    for node, data in G.nodes(data=True):
        node_type = data.get("type", "unknown")
        label = data.get("label", node)
        degree = degrees.get(node, 1)
        net.add_node(node, label=label, color=COLORS.get(node_type, "#888888"),
                     size=10 + degree * 3, title=f"{node_type.upper()}: {label}\nConnections: {degree}")

    for u, v, data in G.edges(data=True):
        weight = data.get("weight", 1)
        reports = ", ".join(data.get("reports", []))
        net.add_edge(u, v, value=weight, title=f"Shared in reports: {reports}")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    net.write_html(OUTPUT_PATH)
    print(f"Graph visualization saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_visualization()