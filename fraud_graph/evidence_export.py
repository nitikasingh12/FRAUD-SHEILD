import json
from datetime import datetime


def build_evidence_package(cluster: dict) -> dict:
    return {
        "package_id": f"EVID-{cluster['central_node'].replace(':', '-')}",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "cluster_summary": {
            "total_linked_entities": cluster["size"],
            "total_linked_reports": cluster["num_reports"],
            "central_entity": cluster["central_node"],
            "central_entity_connections": cluster["central_node_degree"],
        },
        "linked_entities": cluster["members"],
        "notes": (
            "This package was auto-generated from citizen fraud reports "
            "based on shared identifiers across multiple reports. It is "
            "an investigative starting point, not certified legal evidence."
        ),
    }


def export_as_json(cluster: dict) -> str:
    return json.dumps(build_evidence_package(cluster), indent=2)