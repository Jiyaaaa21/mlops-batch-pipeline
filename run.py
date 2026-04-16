import argparse
import logging
import sys
import time
import json
import yaml
import numpy as np
import pandas as pd
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)
    return parser.parse_args()


def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def load_config(path):
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    required = ["seed", "window", "version"]

    for key in required:
        if key not in config:
            raise ValueError(f"Missing config key: {key}")

    return config


def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError("Input file not found")

    # Read raw broken CSV
    df = pd.read_csv(path, header=None)

    if df.empty:
        raise ValueError("Dataset is empty")

    # Fix structure
    df = df[0].str.replace('"', '').str.split(",", expand=True)

    # Set header
    df.columns = df.iloc[0]

    # Remove header row
    df = df[1:].reset_index(drop=True)

    # Validate required column
    if "close" not in df.columns:
        raise ValueError("Missing 'close' column")

    # Convert numeric columns
    numeric_cols = ["open", "high", "low", "close", "volume_btc", "volume_usd"]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Validate close column
    if df["close"].isnull().all():
        raise ValueError("All close values are invalid")

    return df

def process_data(df, window):
    # Rolling mean
    df["rolling_mean"] = df["close"].rolling(window=window).mean()

    # Drop rows where rolling mean is NaN (first window-1 rows)
    df = df.dropna().reset_index(drop=True)

    # Generate signal
    df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)

    return df


def write_metrics(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def main():
    args = parse_args()
    start_time = time.time()

    try:
        setup_logging(args.log_file)
        logging.info("Job started")


        # Load config
        config = load_config(args.config)
        logging.info(f"Config loaded: {config}")

        # Set seed
        np.random.seed(config["seed"])

        # Load dataset
        df = load_data(args.input)
        logging.info(f"Rows loaded: {len(df)}")

        logging.info("Rolling mean computation started")
        df = process_data(df, config["window"])
        logging.info("Signal generation completed")

        signal_rate = df["signal"].mean()

        # Placeholder (processing comes next step)
        output = {
            "version": config["version"],
            "rows_processed": len(df),
            "metric": "signal_rate",
            "value": round(float(signal_rate), 4),
            "latency_ms": int((time.time() - start_time) * 1000),
            "seed": config["seed"],
            "status": "success"
        }
        
        logging.info(f"Total latency: {output['latency_ms']} ms")

        write_metrics(args.output, output)

        logging.info(f"Metrics: {output}")
        logging.info("Job completed successfully")

        print(json.dumps(output))
        sys.exit(0)

    except Exception as e:
        error_output = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }

        write_metrics(args.output, error_output)

        logging.exception("Job failed")
        print(json.dumps(error_output))

        sys.exit(1)


if __name__ == "__main__":
    main()