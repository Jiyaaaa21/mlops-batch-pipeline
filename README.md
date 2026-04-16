# MLOps Batch Pipeline

## Overview

This project implements a minimal, production-oriented MLOps batch pipeline in Python.  
It is designed to demonstrate core engineering principles required in real-world ML systems:

- **Reproducibility** via configuration and deterministic execution
- **Observability** through structured logging and metrics
- **Deployment readiness** using Docker

---

## Architecture

The pipeline follows a simple, modular batch processing flow:

1. Load and validate configuration  
2. Load and validate dataset  
3. Perform rolling mean computation on `close` prices  
4. Generate binary trading signal  
5. Compute metrics and execution latency  
6. Persist outputs (JSON metrics + logs)

---

## Features

- Configuration-driven execution using YAML  
- Deterministic behavior using fixed random seed  
- Robust CSV parsing (handles malformed quoted rows)  
- Rolling window computation with controlled NaN handling  
- Structured metrics output for downstream systems  
- Comprehensive logging for observability  
- Fully containerized for reproducible execution

---

## Project Structure

```
mlops-batch-pipeline/
|__ dataset_view        # to understand dataset structure
├── run.py              # Main pipeline entry point
├── config.yaml         # Configuration (seed, window, version)
├── data.csv            # Input dataset
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container definition
├── README.md           # Documentation
├── metrics.json        # Sample output
├── run.log             # Sample logs
├── .dockerignore       # Docker build optimization
```

## Configuration


Example `config.yaml`:

```yaml
seed: 42
window: 5
version: "v1"

-> Local Execution

python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log

-> Docker Execution

docker build -t mlops-task 
docker run --rm mlops-task

Example Output

{
  "version": "v1",
  "rows_processed": 9996,
  "metric": "signal_rate",
  "value": 0.4991,
  "latency_ms": 130,
  "seed": 42,
  "status": "success"
}

## Error Handling

The pipeline is designed to fail gracefully and provide structured feedback.

Handled scenarios include:
- Missing or inaccessible input files
- Invalid or malformed CSV data
- Missing required columns (e.g., `close`)
- Empty datasets
- Invalid configuration schema

In all failure cases, a structured error response is written to `metrics.json`.

---

## Logging and Observability

Logging captures all key stages of execution:

- Job initialization
- Configuration loading and validation
- Dataset ingestion
- Processing steps (rolling mean, signal generation)
- Metrics summary
- Execution completion status

This ensures traceability and debuggability in production environments.

---

## Reproducibility

The pipeline ensures deterministic outputs by:

- Using a fixed random seed from configuration
- Avoiding non-deterministic operations in processing

Repeated runs with the same inputs produce identical results (excluding latency).

---

## Design Decisions

- **NaN Handling**: Initial `(window - 1)` rows are dropped due to undefined rolling mean
- **Schema Consistency**: Fixed output format for reliable downstream consumption
- **Error Reporting**: Metrics file is written in both success and failure scenarios
- **Separation of Concerns**: Clear distinction between config, data loading, and processing logic

---

## Notes

- No hardcoded paths; all inputs are passed via CLI arguments
- Designed as a minimal but extensible foundation for larger ML pipelines






