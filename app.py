"""Local Flask dashboard and JSON API for the synthetic predictive-maintenance demo."""
from pathlib import Path
import pandas as pd
from flask import Flask, jsonify, render_template, request
from src.predict import predict_one, ROOT

app = Flask(__name__)
DATA_PATH = ROOT / "data" / "iot_sensor_data.csv"

@app.get("/")
def dashboard():
    stats = {"rows": 0, "failures": 0, "failure_rate": 0, "avg_temp": 0, "avg_vibration": 0}
    recent = []
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)
        stats = {"rows": int(len(df)), "failures": int(df.failure.sum()), "failure_rate": round(float(df.failure.mean()*100), 1), "avg_temp": round(float(df.temperature_c.mean()), 1), "avg_vibration": round(float(df.vibration_mm_s.mean()), 2)}
        recent = df.tail(12).drop(columns=["timestamp"]).to_dict(orient="records")
    return render_template("index.html", stats=stats, recent=recent)

@app.get("/api/summary")
def summary():
    if not DATA_PATH.exists(): return jsonify({"error": "Dataset missing. Run python main.py all first."}), 400
    df = pd.read_csv(DATA_PATH)
    return jsonify({"rows": int(len(df)), "failure_count": int(df.failure.sum()), "normal_count": int((df.failure == 0).sum()), "failure_rate_percent": round(float(df.failure.mean()*100), 2), "mean_temperature_c": round(float(df.temperature_c.mean()), 2), "mean_vibration_mm_s": round(float(df.vibration_mm_s.mean()), 2), "note": "Synthetic simulation data; not validated industrial telemetry."})

@app.post("/api/predict")
def api_predict():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict): return jsonify({"error": "Send a JSON object containing sensor readings."}), 400
    try:
        return jsonify(predict_one(payload))
    except (ValueError, TypeError) as exc:
        return jsonify({"error": str(exc)}), 400
    except FileNotFoundError as exc:
        return jsonify({"error": str(exc)}), 503

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
