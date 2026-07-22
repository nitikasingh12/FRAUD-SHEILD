import os
import pandas as pd
import networkx as nx

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE, "data", "fraud_reports.csv")

NODE_TYPES = {
    "phone_number": "phone",
    "upi_id": "upi",
    "bank_account": "account",
    "device_id": "device",
}


def build_graph() -> nx.Graph:
    df = pd.read_csv(DATA_PATH, dtype=str)
    G = nx.Graph()

    for _, row in df.iterrows():
        report_id = row["report_id"]
        entities = []
        for col, node_type in NODE_TYPES.items():
            value = row[col]
            node_id = f"{node_type}:{value}"
            if not G.has_node(node_id):
                G.add_node(node_id, type=node_type, label=value)
            entities.append(node_id)

        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                if G.has_edge(entities[i], entities[j]):
                    G[entities[i]][entities[j]]["weight"] += 1
                    G[entities[i]][entities[j]]["reports"].append(report_id)
                else:
                    G.add_edge(entities[i], entities[j], weight=1, reports=[report_id])
    return G


def analyze_clusters(G: nx.Graph) -> list:
    clusters = []
    for component in nx.connected_components(G):
        if len(component) < 2:
            continue
        subgraph = G.subgraph(component)
        degrees = dict(subgraph.degree())
        central_node = max(degrees, key=degrees.get)

        report_ids = set()
        for u, v, data in subgraph.edges(data=True):
            report_ids.update(data.get("reports", []))

        clusters.append({
            "size": len(component),
            "num_reports": len(report_ids),
            "central_node": central_node,
            "central_node_degree": degrees[central_node],
            "members": sorted(component),
        })

    clusters.sort(key=lambda c: c["num_reports"], reverse=True)
    return clusters


def get_summary() -> dict:
    G = build_graph()
    clusters = analyze_clusters(G)
    return {
        "total_nodes": G.number_of_nodes(),
        "total_edges": G.number_of_edges(),
        "num_clusters": len(clusters),
        "clusters": clusters,
    }


if __name__ == "__main__":
    summary = get_summary()
    print(f"Total entities: {summary['total_nodes']}")
    print(f"Total connections: {summary['total_edges']}")
    print(f"Fraud clusters found: {summary['num_clusters']}")