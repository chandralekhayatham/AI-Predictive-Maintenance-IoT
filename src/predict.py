"""Validated prediction helper used by the CLI and Flask dashboard."""
from pathlib import Path
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "predictive_maintenance.joblib"

def load_bundle():
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Trained model not found. Run: python main.py train")
    return joblib.load(MODEL_PATH)

def predict_one(readings: dict) -> dict:
    bundle = load_bundle()
    features = bundle["features"]
    missing = [f for f in features if f not in readings]
    if missing:
        raise ValueError("Missing sensor field(s): " + ", ".join(missing))
    row = pd.DataFrame([{f: float(readings[f]) for f in features}], columns=features)
    model = bundle["model"]
    label = int(model.predict(row)[0])
    probabilities = model.predict_proba(row)[0]
    classes = list(model.named_steps["classifier"].classes_)
    failure_probability = float(probabilities[classes.index(1)]) if 1 in classes else 0.0
    if label == 1 or failure_probability >= 0.5:
        status, recommendation = "MAINTENANCE RECOMMENDED", "Inspect the equipment and verify readings before taking action."
    elif failure_probability >= 0.3:
        status, recommendation = "MONITOR CLOSELY", "Continue monitoring and schedule a routine inspection if the trend persists."
    else:
        status, recommendation = "NORMAL", "No simulated failure risk detected; continue routine monitoring."
    return {"prediction": label, "status": status, "failure_probability": round(failure_probability, 4), "recommendation": recommendation, "model": bundle["model_name"], "synthetic_data": True}
