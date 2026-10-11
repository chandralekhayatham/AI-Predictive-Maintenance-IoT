# AI-Powered Predictive Maintenance System for IoT Devices

A beginner-friendly, GitHub-ready **virtual simulation** that demonstrates how sensor readings can be used to estimate machine-maintenance risk. It creates synthetic sensor telemetry, trains a Random Forest classifier, reports evaluation metrics, saves charts, offers a CLI prediction and serves a small Flask dashboard/API.

> **Important limitation:** this starter project uses synthetic sensor values and labels generated from simulation rules. High evaluation scores only show that the model learned those synthetic rules. They do not establish accuracy on real machines. Do not use this demo to make real equipment safety or maintenance decisions.

## Features
- Synthetic temperature, vibration, current, pressure and runtime data
- Reproducible simulation with a fixed random seed
- Data validation, missing-value imputation and model training pipeline
- Random Forest binary classifier and accuracy, precision, recall and F1 metrics
- Confusion matrix, feature-importance chart and test predictions
- CLI for simulation, training and individual predictions
- Flask dashboard and JSON prediction endpoint
- Basic automated tests

## Architecture

```text
Synthetic IoT sensor simulator
            ↓
CSV sensor dataset → preprocessing/imputation
            ↓
Random Forest classifier
            ↓
Evaluation metrics + saved model
            ↓
CLI prediction / Flask dashboard / JSON API
            ↓
Demo status + maintenance recommendation
```

## Tech stack
Python 3.10+ (tested design target: Python 3.13), Pandas, NumPy, scikit-learn, Matplotlib, Joblib and Flask. No IoT hardware or GPU is required.

## Folder structure
```text
AI-Predictive-Maintenance-IoT/
├── app.py                    # Flask dashboard and API
├── main.py                   # CLI entry point
├── requirements.txt
├── data/                     # Generated CSV dataset
├── src/
│   ├── simulator.py          # Synthetic telemetry generator
│   ├── train_model.py        # Training and evaluation
│   └── predict.py             # Validated prediction helper
├── models/                   # Saved model (generated locally)
├── outputs/                  # Metrics, charts and predictions
├── templates/index.html      # Dashboard markup
├── static/                   # CSS and JavaScript
└── tests/                    # Starter tests
```

## Setup (Windows PowerShell)
Run these commands from the project root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat`, or use `.venv\Scripts\python.exe` directly.

## Run the project

### 1. Generate data and train the model
```powershell
python main.py all
```
This creates `data/iot_sensor_data.csv`, saves the model in `models/`, and writes evaluation outputs to `outputs/`.

### 2. Test a sample prediction
```powershell
python main.py predict
```
Custom values are supported:
```powershell
python main.py predict --temperature 95 --vibration 6 --current 14 --pressure 3.2 --runtime 7000
```

### 3. Launch the dashboard
```powershell
python main.py dashboard
```
Open `http://127.0.0.1:5000` in your browser. The dashboard is local to your computer.

### 4. API example
Send a `POST` request to `/api/predict` with JSON:
```json
{
  "temperature_c": 90,
  "vibration_mm_s": 5.5,
  "current_a": 13,
  "pressure_bar": 3.4,
  "runtime_hours": 6000
}
```
Summary endpoint: `GET /api/summary`.

### 5. Run tests
```powershell
python -m pytest -q
```
Install pytest first if needed: `pip install pytest`.

## Generated outputs
- `outputs/metrics.json` — train/test counts and evaluation metrics
- `outputs/classification_report.txt` — class-wise precision/recall/F1
- `outputs/confusion_matrix.png` — model test split confusion matrix
- `outputs/feature_importance.png` — relative feature importance
- `outputs/test_predictions.csv` — held-out test predictions

## Dataset note
The simulator is included so this project works without hardware or a downloaded dataset. The failure labels are generated from explicit synthetic rules and random variation. To improve the project, replace the generated CSV with a properly documented public predictive-maintenance dataset, map its columns, and evaluate on a realistic holdout split. Do not compare scores across datasets as if they were directly equivalent.

## Next improvements
1. Add a public dataset adapter and dataset citation.
2. Add time-window trend features and time-aware validation.
3. Add calibration and alert thresholds selected for the use case.
4. Add model versioning and data-drift checks.
5. Deploy only after validating with domain experts and real labelled equipment data.

## Author / proof of work
Add your name, repository URL, screenshots and project demo link here before publishing. Capture the dataset preview, training metrics, confusion matrix, feature importance, CLI prediction, dashboard and GitHub repository page.
