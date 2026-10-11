"""Create clearly labelled synthetic machine sensor data for learning/demo use."""
from pathlib import Path
import numpy as np
import pandas as pd

FEATURES = ["temperature_c", "vibration_mm_s", "current_a", "pressure_bar", "runtime_hours"]

def generate_sensor_data(n_rows: int = 2500, random_state: int = 42) -> pd.DataFrame:
    """Generate plausible-looking synthetic readings; labels are rule-based, not real failures."""
    if n_rows < 100:
        raise ValueError("n_rows must be at least 100")
    rng = np.random.default_rng(random_state)
    temperature = rng.normal(62, 8, n_rows).clip(25, 110)
    vibration = rng.normal(2.4, 0.8, n_rows).clip(0.1, 9)
    current = rng.normal(8.5, 1.6, n_rows).clip(1, 18)
    pressure = rng.normal(5.2, 0.65, n_rows).clip(1.5, 9)
    runtime = rng.uniform(10, 10000, n_rows)
    # Inject a minority of degraded operating states to create useful examples.
    degraded = rng.random(n_rows) < 0.22
    temperature[degraded] += rng.uniform(8, 24, degraded.sum())
    vibration[degraded] += rng.uniform(1.0, 3.5, degraded.sum())
    current[degraded] += rng.uniform(0.8, 3.5, degraded.sum())
    pressure[degraded] += rng.normal(-0.8, 0.4, degraded.sum())
    # Label is a transparent simulation rule, not a real-world ground-truth label.
    risk_signal = ((temperature > 82) | (vibration > 4.8) | (current > 12.5) | (pressure < 3.7))
    failure = (risk_signal & (rng.random(n_rows) < 0.82)) | (degraded & (rng.random(n_rows) < 0.12))
    df = pd.DataFrame({
        "timestamp": pd.date_range("2026-01-01", periods=n_rows, freq="h"),
        "temperature_c": temperature.round(2),
        "vibration_mm_s": vibration.round(3),
        "current_a": current.round(3),
        "pressure_bar": pressure.round(3),
        "runtime_hours": runtime.round(1),
        "failure": failure.astype(int),
    })
    return df

def save_dataset(path: str | Path = "data/iot_sensor_data.csv", n_rows: int = 2500) -> pd.DataFrame:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df = generate_sensor_data(n_rows=n_rows)
    df.to_csv(path, index=False)
    return df

if __name__ == "__main__":
    df = save_dataset()
    print(f"Generated {len(df):,} synthetic sensor rows")
    print(df.head().to_string(index=False))
    print("\nFailure label counts:")
    print(df["failure"].value_counts().sort_index().rename(index={0: "normal", 1: "simulated failure"}))
