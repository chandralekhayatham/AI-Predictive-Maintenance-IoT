import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.simulator import generate_sensor_data

def test_simulator_schema_and_labels():
    df = generate_sensor_data(300, 7)
    assert len(df) == 300
    assert {"temperature_c", "vibration_mm_s", "current_a", "pressure_bar", "runtime_hours", "failure"}.issubset(df.columns)
    assert set(df.failure.unique()).issubset({0, 1})

def test_simulator_reproducible():
    a = generate_sensor_data(150, 12)
    b = generate_sensor_data(150, 12)
    assert a.equals(b)

def test_simulator_rejects_too_few_rows():
    try:
        generate_sensor_data(10)
        assert False, "Expected ValueError"
    except ValueError:
        pass
