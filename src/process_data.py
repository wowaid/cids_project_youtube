import os
import time
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "youtube")
DB_USER = os.getenv("DB_USER", "youtube")
DB_PASSWORD = os.getenv("DB_PASSWORD", "youtube")
PROCESS_TABLE = os.getenv("PROCESS_TABLE", "videos")

BASE_DIR = Path(__file__).resolve().parent
if (BASE_DIR / "sql").exists():
    SQL_DIR = BASE_DIR / "sql"
else:
    SQL_DIR = BASE_DIR.parent / "sql"

if (BASE_DIR / "results").exists():
    RESULTS_DIR = BASE_DIR / "results"
else:
    RESULTS_DIR = BASE_DIR.parent / "results"

RESULTS_DIR.mkdir(exist_ok=True)


def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


def run_query(engine, sql_file):
    sql_path = SQL_DIR / sql_file

    print(f"\nRunning {sql_file}...")

    start = time.perf_counter()

    df = pd.read_sql(
        sql_path.read_text(),
        engine
    )

    elapsed = time.perf_counter() - start

    output_name = sql_file.replace(".sql", ".csv")
    output_path = RESULTS_DIR / output_name

    df.to_csv(output_path, index=False)

    print(f"Rows: {len(df):,}")
    print(f"Time: {elapsed:.4f} seconds")
    print(f"Saved to: {output_path}")

    return elapsed


def main():
    print("=" * 60)
    print("CIDS — YouTube Data Processing")
    print("=" * 60)

    engine = get_engine()

    queries = [
        "01_country_uniqueness.sql",
        "02_music_gaming.sql",
        "03_drama_score.sql",
        "04_longest_trending.sql",
        "05_time_to_trend.sql",
        "06_shouty_titles.sql",
    ]

    timings = []

    for query in queries:
        elapsed = run_query(engine, query)

        timings.append({
            "query": query,
            "processing_time_seconds": elapsed
        })

    timings_df = pd.DataFrame(timings)

    timings_df.to_csv(
        RESULTS_DIR / "processing_times.csv",
        index=False
    )

    print("\nProcessing completed.")
    print("\nTiming summary:")
    print(timings_df)


if __name__ == "__main__":
    main()