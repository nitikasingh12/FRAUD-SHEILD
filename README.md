# Citizen Fraud Shield

An AI-powered Digital Public Safety platform built for the ET AI Hackathon 2026, addressing the "AI for Digital Public Safety: Defeating Counterfeiting, Fraud & Digital Arrest Scams" problem statement.

The platform combines a hybrid rule-based + ML fraud text classifier, a computer vision counterfeit currency detector, a fraud network graph engine, and a geospatial crime hotspot map into a single working prototype — with automated alerting and evidence export for investigative auditability.

## Live Modules

| Module | What it does | Route |
|---|---|---|
| **Citizen Fraud Shield** | Assesses risk of scam messages/calls (digital arrest scams, phishing, OTP fraud) using a hybrid rule engine + TF-IDF/Logistic Regression classifier | `/` |
| **Counterfeit Currency Check** | Classifies uploaded currency note images as real/fake using OpenCV feature extraction (color histograms, edge density, texture/LBP) + RandomForest | `/currency` |
| **Fraud Network Intelligence** | Builds a graph from citizen fraud reports (phone/UPI/account/device links) to detect coordinated fraud rings vs isolated incidents, with evidence export | `/fraud-network` |
| **Crime Hotspot Map** | Interactive heatmap of fraud complaints, digital arrest scams, and counterfeit seizures across Indian cities | `/crime-map` |
| **Alert Log** | Auto-generated alerts for every High-risk scam detection (simulates MHA notification) | `/alerts` |

All pages are behind a simple login gate (demo credentials below).

## Setup (Windows / VS Code)

1. Clone this repo and open it in VS Code
2. Create and activate a virtual environment:

python -m venv venv
venv\Scripts\activate

3. Install dependencies:

pip install -r requirements.txt

4. Train the fraud-text classifier:

python train_model.py

5. Generate the counterfeit currency dataset and train the detector:

cd counterfeit
python generate_dummy_data.py
python train_sklearn.py
cd ..

6. Generate the fraud network graph visualization:

cd fraud_graph
python visualize.py
cd ..

7. Generate the crime hotspot map:

cd geospatial
python map_engine.py
cd ..

8. Run the app:

python app.py

9. Open `http://127.0.0.1:5000` and log in:
   - **Username:** `officer`
   - **Password:** `demo123`

## Project Structure

fraud-shield/
├── app.py # Flask app, routes, login
├── train_model.py # Trains the fraud-text classifier
├── requirements.txt
├── data/
│ └── messages.csv # Scam vs legit training data
├── models/
│ └── scam_model.joblib # Created after training
├── scam_engine/
│ ├── rules.py # Keyword/pattern rule engine
│ ├── classifier.py # TF-IDF + Logistic Regression
│ ├── scorer.py # Combines rules + ML into a verdict
│ └── alerting.py # Auto-logs High-risk alerts
├── counterfeit/
│ ├── generate_dummy_data.py # Synthetic placeholder images (pipeline testing)
│ ├── features.py # OpenCV/LBP feature extraction
│ ├── train_sklearn.py # RandomForest training
│ ├── predict_sklearn.py # Loads model, predicts real/fake
│ └── data/, model/
├── fraud_graph/
│ ├── data/fraud_reports.csv # Synthetic linked fraud reports
│ ├── graph_engine.py # Builds graph, detects clusters
│ ├── visualize.py # Interactive pyvis visualization
│ └── evidence_export.py # Structured evidence package export
├── geospatial/
│ ├── data/crime_locations.csv # Synthetic incident locations
│ └── map_engine.py # Folium heatmap + markers
├── templates/ # All page templates + login.html
└── static/ # CSS, JS, generated HTML visualizations


## Design Notes & Honest Tradeoffs

- **Counterfeit detection uses OpenCV + RandomForest, not a CNN.** This was a deliberate choice after hitting TensorFlow DLL/AVX compatibility issues on Windows — hand-engineered features (color histograms, edge density, Local Binary Pattern texture, quadrant-wise analysis) are more reliable to ship and still demonstrate real computer vision. A CNN is the natural next step with more time and a GPU-friendly environment.
- **Currency and fraud-report datasets are synthetic placeholders**, generated to prove the pipeline works end-to-end. Before production use, these should be replaced with real datasets (e.g. Kaggle's Fake Currency Detection Dataset, or real NCRB fraud report data).
- **The false-positive rate for citizen-facing tools was a specific design target.** The rule engine includes negation detection (e.g. "please do not share your OTP" is correctly *not* flagged, since it's a warning, not a scam request) — this was validated against a set of legitimate-but-urgent test messages (flight check-ins, bank card renewals, exam alerts) to avoid crying wolf on real communications.
- **Login is a demo-only gate** (hardcoded credentials, Flask session), not production authentication — sufficient to demonstrate access control for a prototype, not a real auth system.
- **Evidence export is investigative-starting-point level**, not certified legal evidence — real court admissibility would require signed/timestamped source data and case management system integration.

## Future Scope

- Multi-channel citizen access (WhatsApp, IVR) and 12 regional language support
- Deepfake/voice spoofing detection for call-based scams
- CNN-based counterfeit detection once trained on the full real dataset
- Neo4j-backed fraud graph for production-scale relationship queries
- Real-time integration with NCRB and MHA alerting systems

## Hackathon Submission

Built for: **ET AI Hackathon 2026** — Problem Statement: *AI for Digital Public Safety: Defeating Counterfeiting, Fraud & Digital Arrest Scams*

