import os
import json
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
ALERT_LOG_PATH = os.path.join(BASE, "alert_log.json")


def _load_alerts() -> list:
    if not os.path.exists(ALERT_LOG_PATH):
        return []
    with open(ALERT_LOG_PATH, "r") as f:
        return json.load(f)


def _save_alerts(alerts: list):
    with open(ALERT_LOG_PATH, "w") as f:
        json.dump(alerts, f, indent=2)


def log_alert(message_text: str, assessment: dict) -> dict:
    if assessment.get("risk_level") != "High":
        return None

    alert = {
        "alert_id": f"ALERT-{int(datetime.utcnow().timestamp())}",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "risk_score": assessment.get("risk_score"),
        "matched_categories": assessment.get("matched_categories"),
        "message_excerpt": message_text[:200],
        "status": "Flagged for MHA notification (simulated)",
    }

    alerts = _load_alerts()
    alerts.insert(0, alert)
    _save_alerts(alerts)
    return alert


def get_recent_alerts(limit: int = 20) -> list:
    return _load_alerts()[:limit]