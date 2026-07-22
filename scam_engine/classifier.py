import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "messages.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "scam_model.joblib")


def train():
    df = pd.read_csv(DATA_PATH)
    X = df["text"]
    y = (df["label"] == "scam").astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words="english")),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ])

    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    print("Evaluation on held-out test split:")
    print(classification_report(y_test, preds, target_names=["legit", "scam"]))

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


def predict_proba(text: str) -> float:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("No trained model found. Run `python train_model.py` first.")
    pipeline = joblib.load(MODEL_PATH)
    proba = pipeline.predict_proba([text])[0][1]
    return float(proba)


if __name__ == "__main__":
    train()