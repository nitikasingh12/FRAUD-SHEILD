import os
import glob
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from features import extract_features

BASE = os.path.dirname(os.path.abspath(__file__))
TRAIN_DIR = os.path.join(BASE, "data", "train")
VAL_DIR = os.path.join(BASE, "data", "val")
MODEL_PATH = os.path.join(BASE, "model", "currency_rf.joblib")


def load_split(folder):
    X, y = [], []
    for label, class_name in enumerate(["fake", "real"]):
        pattern = os.path.join(folder, class_name, "*")
        for path in glob.glob(pattern):
            try:
                X.append(extract_features(path))
                y.append(label)
            except ValueError:
                print(f"Skipping unreadable file: {path}")
    return np.array(X), np.array(y)


def train():
    print("Extracting features from training set...")
    X_train, y_train = load_split(TRAIN_DIR)
    print("Extracting features from validation set...")
    X_val, y_val = load_split(VAL_DIR)
    print(f"Train samples: {len(X_train)}, Val samples: {len(X_val)}")

    clf = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, class_weight="balanced")
    clf.fit(X_train, y_train)

    preds = clf.predict(X_val)
    print("Evaluation on validation set:")
    print(classification_report(y_val, preds, target_names=["fake", "real"]))

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train()