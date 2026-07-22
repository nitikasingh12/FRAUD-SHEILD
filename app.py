import os
from functools import wraps
from flask import Flask, render_template, request, jsonify, Response, session, redirect, url_for
from werkzeug.utils import secure_filename

from scam_engine.scorer import assess
from scam_engine.alerting import log_alert, get_recent_alerts
from counterfeit.predict_sklearn import predict_image
from fraud_graph.graph_engine import get_summary as get_fraud_network_summary
from fraud_graph.evidence_export import export_as_json
from geospatial.map_engine import get_summary as get_crime_map_summary

app = Flask(__name__)
app.secret_key = "hackathon-demo-secret-key-2026"  # fine for a prototype demo

DEMO_USERNAME = "officer"
DEMO_PASSWORD = "demo123"

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == DEMO_USERNAME and password == DEMO_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("index"))
        return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/api/assess", methods=["POST"])
def api_assess():
    data = request.get_json(force=True)
    text = (data.get("message") or "").strip()
    if not text:
        return jsonify({"error": "Message cannot be empty"}), 400
    result = assess(text)
    log_alert(text, result)
    return jsonify(result)


@app.route("/alerts")
@login_required
def alerts_page():
    alerts = get_recent_alerts()
    return render_template("alerts.html", alerts=alerts)


@app.route("/currency")
@login_required
def currency_page():
    return render_template("currency.html")


@app.route("/api/currency-check", methods=["POST"])
def api_currency_check():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    file = request.files["image"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Please upload a valid image file (png/jpg/jpeg)"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        result = predict_image(filepath)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

    return jsonify(result)


@app.route("/fraud-network")
@login_required
def fraud_network_page():
    summary = get_fraud_network_summary()
    return render_template("fraud_network.html", summary=summary)


@app.route("/api/evidence/<int:cluster_index>")
def api_evidence_export(cluster_index):
    summary = get_fraud_network_summary()
    clusters = summary["clusters"]
    if cluster_index < 0 or cluster_index >= len(clusters):
        return jsonify({"error": "Cluster not found"}), 404
    package_json = export_as_json(clusters[cluster_index])
    return Response(package_json, mimetype="application/json")


@app.route("/crime-map")
@login_required
def crime_map_page():
    summary = get_crime_map_summary()
    return render_template("crime_map.html", summary=summary)


if __name__ == "__main__":
    app.run(debug=True, port=5000)