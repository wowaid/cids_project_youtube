import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")

countries = [
    "CA",
    "DE",
    "FR",
    "GB",
    "IN",
    "JP",
    "KR",
    "MX",
    "RU",
    "US"
]

columns = [
    "video_id",
    "trending_date",
    "title",
    "channel_title",
    "category_id",
    "publish_time",
    "views",
    "likes",
    "dislikes",
    "comment_count"
]

samples = []

for country in countries:
    print(f"Processing {country}...")

    file_path = DATA_DIR / f"{country}videos.csv"

    df = pd.read_csv(
        file_path,
        encoding="utf-8",
        encoding_errors="replace"
    )

    # Keep only the columns needed for the project
    df = df[columns].copy()

    # Add country information
    df["country"] = country

    # Take the same number of observations from every country
    n = min(20000, len(df))

    sample = df.sample(
        n=n,
        random_state=42
    )

    samples.append(sample)

# Combine all countries
result = pd.concat(samples, ignore_index=True)

# Shuffle the final dataset
result = result.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# Save compact dataset
output_path = DATA_DIR / "youtube_trending.csv"

result.to_csv(
    output_path,
    index=False
)

print("\nDataset created successfully!")
print(f"Rows: {len(result):,}")
print(f"Columns: {len(result.columns)}")
print(f"Saved to: {output_path}")
print(f"Size: {output_path.stat().st_size / (1024 * 1024):.2f} MB")