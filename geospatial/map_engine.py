import os
import pandas as pd
import folium
from folium.plugins import HeatMap

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE, "data", "crime_locations.csv")
OUTPUT_PATH = os.path.join(os.path.dirname(BASE), "static", "crime_map.html")

TYPE_COLORS = {"digital_arrest_scam": "red", "fraud_complaint": "orange", "counterfeit_seizure": "purple"}
TYPE_LABELS = {"digital_arrest_scam": "Digital Arrest Scam", "fraud_complaint": "Fraud Complaint", "counterfeit_seizure": "Counterfeit Seizure"}


def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def get_summary() -> dict:
    df = load_data()
    by_type = df["incident_type"].value_counts().to_dict()
    by_city = df.groupby("city").size().sort_values(ascending=False)
    hotspot_city = by_city.index[0]
    hotspot_count = int(by_city.iloc[0])

    return {
        "total_incidents": len(df),
        "by_type": {TYPE_LABELS.get(k, k): v for k, v in by_type.items()},
        "hotspot_city": hotspot_city,
        "hotspot_count": hotspot_count,
    }


def generate_map():
    df = load_data()
    center_lat, center_lon = df["lat"].mean(), df["lon"].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=5, tiles="CartoDB positron")

    heat_data = [[row["lat"], row["lon"]] for _, row in df.iterrows()]
    HeatMap(heat_data, radius=25, blur=15).add_to(m)

    severity_radius = {"high": 9, "medium": 6, "low": 4}
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=severity_radius.get(row["severity"], 5),
            color=TYPE_COLORS.get(row["incident_type"], "gray"),
            fill=True, fill_opacity=0.75,
            popup=f"<b>{TYPE_LABELS.get(row['incident_type'], row['incident_type'])}</b><br>City: {row['city']}<br>Severity: {row['severity']}",
        ).add_to(m)

    legend_html = """
    <div style="position: fixed; bottom: 30px; left: 30px; z-index: 1000;
                background: white; padding: 12px 16px; border-radius: 8px;
                border: 1px solid #ccc; font-family: sans-serif; font-size: 13px;">
        <b>Incident Type</b><br>
        <span style="color:red;">&#9679;</span> Digital Arrest Scam<br>
        <span style="color:orange;">&#9679;</span> Fraud Complaint<br>
        <span style="color:purple;">&#9679;</span> Counterfeit Seizure
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    m.save(OUTPUT_PATH)
    print(f"Crime map saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_map()