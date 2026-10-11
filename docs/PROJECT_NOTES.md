# Project notes

## Problem statement
Equipment condition can be monitored through measurements such as temperature, vibration, electrical current and pressure. This educational prototype shows the data-to-model-to-alert workflow without physical sensors.

## Design decision
This first version uses a Random Forest classifier because it is lightweight, explainable enough for a student demonstration, and works on tabular data. The uploaded guide mentions LSTM in one section but its sample training code uses Random Forest; this implementation intentionally follows the beginner-friendly Random Forest sample.

## Workflow
1. Generate simulated telemetry with a reproducible seed.
2. Inspect sensor features and simulated labels.
3. Split rows into train/test sets with stratification.
4. Impute missing values and train a Random Forest pipeline.
5. Evaluate accuracy, precision, recall and F1 on the held-out synthetic split.
6. Save the trained pipeline, metrics and charts.
7. Use the CLI or local Flask dashboard/API to score a sensor reading.

## Responsible interpretation
The synthetic label rule is correlated with simulated sensor thresholds by design. Model performance is therefore not evidence of real-world failure prediction. For real use, collect appropriately consented/authorized, timestamped machine telemetry and verified maintenance outcomes; split by machine/time to avoid leakage; assess false negatives and false positives with engineering stakeholders; and validate safely before any operational integration.
