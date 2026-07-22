import os
import joblib

try:
    from .features import extract_features
except ImportError:
    from features import extract_features

BASE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE, "model", "currency_rf.joblib")

_model = None


def _get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("No trained model found. Run `python train_sklearn.py` first.")
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_image(image_path: str) -> dict:
    model = _get_model()
    features = extract_features(image_path).reshape(1, -1)

    proba = model.predict_proba(features)[0]
    pred_class = model.predict(features)[0]

    label = "real" if pred_class == 1 else "fake"
    confidence = proba[pred_class] * 100

    return {
        "label": label,
        "confidence": round(float(confidence), 1),
        "raw_score": round(float(proba[1]), 4),
    }