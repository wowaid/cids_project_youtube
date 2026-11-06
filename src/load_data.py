import os
import time
import urllib.request

import pandas as pd
from sqlalchemy import create_engine


DATA_URL = "https://raw.githubusercontent.com/wowaid/cids_project_youtube/main/data/youtube_trending.csv"

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "youtube")
DB_USER = os.getenv("DB_USER", "youtube")
DB_PASSWORD = os.getenv("DB_PASSWORD", "youtube")


def wait_for_database():
    """Wait until PostgreSQL is ready."""
    print("Waiting for PostgreSQL...")

    for attempt in range(30):
        try:
            engine = create_engine(
                f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
                f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            )

            with engine.connect():
                print("PostgreSQL is ready!")
                return engine

        except Exception:
            print(f"Database not ready yet ({attempt + 1}/30)")
            time.sleep(2)

    raise RuntimeError("Could not connect to PostgreSQL.")


def download_dataset():
    """Download the dataset from GitHub."""
    output_path = "/tmp/youtube_trending.csv"

    print("Downloading dataset from GitHub...")

    urllib.request.urlretrieve(DATA_URL, output_path)

    print("Dataset downloaded.")

    return output_path


def load_data(engine, csv_path):
    """Load CSV data into PostgreSQL."""
    print("Reading CSV...")

    df = pd.read_csv(csv_path)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("Loading data into PostgreSQL...")

    df.to_sql(
        "videos",
        engine,
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=5000
    )

    print("Data loaded successfully!")


def main():
    engine = wait_for_database()

    csv_path = download_dataset()

    load_data(engine, csv_path)

    print("Finished!")


if __name__ == "__main__":
    main()