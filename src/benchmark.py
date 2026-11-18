import os
import time
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "youtube")
DB_USER = os.getenv("DB_USER", "youtube")
DB_PASSWORD = os.getenv("DB_PASSWORD", "youtube")

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent / "data" / "youtube_trending.csv"
RESULTS_DIR = BASE_DIR.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

REPEATS = 3


def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


def get_table_size(engine):
    query = text("""
        SELECT pg_total_relation_size('benchmark_videos')
    """)

    with engine.connect() as connection:
        size_bytes = connection.execute(query).scalar()

    return size_bytes


def format_size(size_bytes):
    size_mb = size_bytes / (1024 * 1024)
    return round(size_mb, 2)


def load_sample(engine, dataframe):
    dataframe.to_sql(
        "benchmark_videos",
        engine,
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=5000
    )


def process_sample(engine):
    queries = {
        "country_uniqueness": """
            SELECT
                country,
                COUNT(DISTINCT video_id) AS unique_videos
            FROM benchmark_videos
            GROUP BY country
            ORDER BY country
        """,

        "average_views": """
            SELECT
                country,
                AVG(views) AS average_views
            FROM benchmark_videos
            GROUP BY country
            ORDER BY country
        """,

        "engagement": """
            SELECT
                country,
                AVG(likes) AS average_likes,
                AVG(comment_count) AS average_comments
            FROM benchmark_videos
            GROUP BY country
            ORDER BY country
        """
    }

    total_processing_time = 0

    for query in queries.values():
        start = time.perf_counter()

        with engine.connect() as connection:
            pd.read_sql(text(query), connection)

        elapsed = time.perf_counter() - start
        total_processing_time += elapsed

    return total_processing_time


def run_experiment(engine, df, label, fraction):
    sample_size = int(len(df) * fraction)
    sample = df.head(sample_size)

    print("\n" + "-" * 60)
    print(f"Experiment: {label}")
    print(f"Rows: {sample_size:,}")

    run_results = []

    for run in range(1, REPEATS + 1):
        print(f"\nRun {run}/{REPEATS}")

        # Load measurement
        load_start = time.perf_counter()

        load_sample(engine, sample)

        load_time = time.perf_counter() - load_start

        # Processing measurement
        process_start = time.perf_counter()

        processing_time = process_sample(engine)

        total_time = load_time + processing_time

        table_size = get_table_size(engine)

        print(f"Load time:       {load_time:.4f} seconds")
        print(f"Processing time: {processing_time:.4f} seconds")
        print(f"Total time:      {total_time:.4f} seconds")
        print(f"Table size:      {format_size(table_size)} MB")

        run_results.append({
            "run": run,
            "load_time_seconds": load_time,
            "processing_time_seconds": processing_time,
            "total_time_seconds": total_time,
            "table_size_mb": format_size(table_size)
        })

    # Calculate averages
    avg_load = sum(r["load_time_seconds"] for r in run_results) / REPEATS
    avg_processing = sum(r["processing_time_seconds"] for r in run_results) / REPEATS
    avg_total = sum(r["total_time_seconds"] for r in run_results) / REPEATS
    avg_size = sum(r["table_size_mb"] for r in run_results) / REPEATS

    print("\nAverage:")
    print(f"Load time:       {avg_load:.4f} seconds")
    print(f"Processing time: {avg_processing:.4f} seconds")
    print(f"Total time:      {avg_total:.4f} seconds")
    print(f"Table size:      {avg_size:.2f} MB")

    return {
        "data_size": label,
        "rows": sample_size,
        "avg_load_time_seconds": round(avg_load, 4),
        "avg_processing_time_seconds": round(avg_processing, 4),
        "avg_total_time_seconds": round(avg_total, 4),
        "avg_table_size_mb": round(avg_size, 2)
    }


def main():
    print("=" * 60)
    print("CIDS — Pipeline Benchmark")
    print("=" * 60)

    print("\nLoading dataset from:")
    print(DATA_PATH)

    df = pd.read_csv(DATA_PATH)

    total_rows = len(df)

    print(f"Total rows: {total_rows:,}")
    print(f"Repeats per size: {REPEATS}")

    engine = get_engine()

    experiments = [
        ("25%", 0.25),
        ("50%", 0.50),
        ("100%", 1.00),
    ]

    results = []

    for label, fraction in experiments:
        result = run_experiment(engine, df, label, fraction)
        results.append(result)

    results_df = pd.DataFrame(results)

    output_path = RESULTS_DIR / "benchmark_results.csv"
    results_df.to_csv(output_path, index=False)

    print("\n" + "=" * 60)
    print("Benchmark completed")
    print("=" * 60)

    print("\nFinal results:")
    print(results_df.to_string(index=False))

    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()