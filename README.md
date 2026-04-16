# MLOps Batch Pipeline Task

This project implements a minimal MLOps-style batch pipeline in Python.

Features:
- Config-driven execution using YAML
- Deterministic runs using fixed seed
- Rolling mean computation and signal generation
- Structured metrics output (JSON)
- Detailed logging for observability
- Fully Dockerized for reproducible execution

1. Project Structure

mlops-batch-pipeline/

│__ dataset_view.py        # to understand dataset structure
├── run.py                 # Main pipeline (entry point)
├── config.yaml            # Config (seed, window, version)
├── data.csv               # Input dataset
├── requirements.txt       # Dependencies
├── Dockerfile             # Docker setup
├── README.md              # Documentation
│
├── metrics.json           # Sample output (success case)
├── run.log                # Sample logs
│
├── .dockerignore          # Ignore unnecessary files in Docker


2. Local Execution

python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log

3. Docker Execution

docker build -t mlops-task .
docker run --rm mlops-task

4. Example Output

{
  "version": "v1",
  "rows_processed": 9996,
  "metric": "signal_rate",
  "value": 0.4991,
  "latency_ms": 130,
  "seed": 42,
  "status": "success"
}

5. Key Design Decisions

- First (window-1) rows are dropped due to undefined rolling mean
- CSV parsing includes handling malformed quoted rows
- Metrics are written in both success and error cases
- Logging captures all major pipeline steps for observability
- Seed ensures deterministic behavior across runs


