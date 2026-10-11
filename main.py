"""Command-line entry point: simulate, train, predict, or launch the dashboard."""
import argparse
import json
from pathlib import Path
from src.simulator import save_dataset
from src.train_model import train
from src.predict import predict_one, ROOT

def main():
    parser = argparse.ArgumentParser(description="Virtual IoT predictive maintenance demo")
    parser.add_argument("command", choices=["all", "simulate", "train", "predict", "dashboard"], help="Action to run")
    parser.add_argument("--temperature", type=float, default=90.0, help="Temperature in degrees C")
    parser.add_argument("--vibration", type=float, default=5.5, help="Vibration in mm/s")
    parser.add_argument("--current", type=float, default=13.0, help="Current in A")
    parser.add_argument("--pressure", type=float, default=3.4, help="Pressure in bar")
    parser.add_argument("--runtime", type=float, default=6000.0, help="Runtime in hours")
    args = parser.parse_args()
    if args.command in ("all", "simulate"):
        df = save_dataset(ROOT / "data" / "iot_sensor_data.csv")
        print(f"Saved {len(df)} synthetic sensor records to data/iot_sensor_data.csv")
    if args.command in ("all", "train"):
        if not (ROOT / "data" / "iot_sensor_data.csv").exists(): save_dataset(ROOT / "data" / "iot_sensor_data.csv")
        train()
    if args.command == "predict":
        readings = {"temperature_c": args.temperature, "vibration_mm_s": args.vibration, "current_a": args.current, "pressure_bar": args.pressure, "runtime_hours": args.runtime}
        print(json.dumps({"sensor_readings": readings, **predict_one(readings)}, indent=2))
    if args.command == "dashboard":
        from app import app
        app.run(host="127.0.0.1", port=5000, debug=False)

if __name__ == "__main__": main()
