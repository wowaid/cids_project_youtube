# CIDS — YouTube Trending Data Processing Infrastructure

## 1. Project Overview

This project implements a small reproducible data processing system for the **Trending YouTube Video Statistics** dataset.

The main goal is to build a complete data pipeline that can:

- obtain a public dataset;
- store it in a PostgreSQL database;
- process it using SQL and Python;
- generate analytical results;
- run the complete pipeline with Docker Compose;
- measure system performance as the dataset size increases.

The project focuses on **data infrastructure, reproducibility and performance measurement** rather than on building a large application or dashboard.

---

## 2. Research Questions

The system processes the dataset to answer six analytical questions:

1. Which country has the most unique Trending videos?
2. Which countries are the most music-obsessed and gaming-obsessed?
3. What is the most dramatic trending video?
4. Which video stayed on the Trending chart for the longest period?
5. How many days pass between publishing and trending?
6. Do shouty titles receive more views?

Each question is implemented as an SQL query executed against PostgreSQL.

---

## 3. Dataset

### Source

The project uses the **Trending YouTube Video Statistics** dataset by Mitchell J. (2017–2018).

The original dataset contains YouTube Trending video statistics for 10 countries:

- Canada
- Germany
- France
- Great Britain
- India
- Japan
- South Korea
- Mexico
- Russia
- United States

Original dataset:

https://www.kaggle.com/datasets/datasnaek/youtube-new

### Project Dataset

For this project, the original country-specific files were combined into one compact dataset:

```text
data/youtube_trending.csv
```

The project dataset contains:

- **200,000 rows**
- **11 columns**
- approximately **30 MB**

The compact dataset is stored in GitHub and is downloaded automatically by the Docker loader.

Dataset URL:

```text
https://raw.githubusercontent.com/wowaid/cids_project_youtube/main/data/youtube_trending.csv
```

---

## 4. System Architecture

The system follows the following data flow:

```text
                  PUBLIC DATASET
                        |
                        v
                   GitHub CSV
                        |
                        v
              +-------------------+
              |      Loader       |
              |  Docker container |
              +---------+---------+
                        |
                        v
              +-------------------+
              |    PostgreSQL     |
              |      Database     |
              +---------+---------+
                        |
                        v
              +-------------------+
              |     Processor     |
              |    Python + SQL   |
              +---------+---------+
                        |
                        v
                  CSV RESULTS
                        |
                        v
                  MEASUREMENTS
```

The system can be viewed as five stages:

**GET → STORE → PROCESS → SHOW → MEASURE**

- **GET** — download the dataset from GitHub.
- **STORE** — load the data into PostgreSQL.
- **PROCESS** — execute analytical SQL queries.
- **SHOW** — save query results as CSV files.
- **MEASURE** — benchmark loading, processing and storage.

Docker Compose manages the complete infrastructure.

---

## 5. Database

### Why PostgreSQL?

PostgreSQL was selected because the dataset is structured tabular data and the analytical tasks require:

- filtering;
- grouping;
- aggregation;
- joins;
- date calculations;
- ranking.

PostgreSQL also provides database size measurements through functions such as `pg_database_size()`, which are used in the performance evaluation.

### Database Structure

The database is called:

```text
youtube
```

The main tables are:

### `videos`

Contains the YouTube Trending records.

Important fields include:

```text
video_id
trending_date
title
channel_title
category_id
publish_time
views
likes
dislikes
comment_count
country
```

### `categories`

Contains the category mapping:

```text
category_id
category_name
```

The tables are connected through `category_id`.

---

## 6. Processing

Processing is implemented with **Python, pandas, SQLAlchemy and PostgreSQL**.

Six SQL queries are stored in the `sql/` directory:

```text
sql/
├── 01_country_uniqueness.sql
├── 02_music_gaming.sql
├── 03_drama_score.sql
├── 04_longest_trending.sql
├── 05_time_to_trend.sql
└── 06_shouty_titles.sql
```

### Query 1 — Country Uniqueness

Calculates the number and percentage of videos that appear uniquely in a country's Trending data.

### Query 2 — Music and Gaming

Calculates the share of Trending videos belonging to Music and Gaming categories.

### Query 3 — Drama Score

Uses:

```text
DramaScore = 1000 × comment_count / views
```

to identify videos with a high comment-to-view ratio.

### Query 4 — Longest Trending

Calculates the observed period between the first and last Trending dates for each video.

### Query 5 — Time to Trend

Calculates the number of days between publication and the first observed Trending date.

### Query 6 — Shouty Titles

Identifies titles with a high uppercase-character ratio or multiple exclamation marks.

---

## 7. Docker Infrastructure

The project uses Docker Compose with three services:

```text
postgres
   |
   +-- PostgreSQL database

loader
   |
   +-- downloads and loads the dataset

processor
   |
   +-- executes SQL queries and saves results
```

The startup order is controlled by a PostgreSQL health check and service dependencies:

```text
PostgreSQL healthy
        |
        v
      Loader
        |
        v
    Processor
```

The complete pipeline can be started with one command:

```bash
docker compose up --build
```

No local PostgreSQL installation is required.

---

## 8. Project Structure

```text
cids_project_youtube/
|
├── data/
│   └── youtube_trending.csv
|
├── docker/
│   ├── Dockerfile
│   └── Dockerfile.processor
|
├── sql/
│   ├── 01_country_uniqueness.sql
│   ├── 02_music_gaming.sql
│   ├── 03_drama_score.sql
│   ├── 04_longest_trending.sql
│   ├── 05_time_to_trend.sql
│   └── 06_shouty_titles.sql
|
├── src/
│   ├── load_data.py
│   ├── process_data.py
│   └── benchmark.py
|
├── results/
│   ├── processing_times.csv
│   ├── benchmark_results.csv
│   └── query result CSV files
|
├── docker-compose.yml
├── create_dataset.py
├── README.md
└── .gitignore
```

---

## 9. Measurements

Performance was measured using three dataset sizes:

- **25%** — 50,000 rows
- **50%** — 100,000 rows
- **100%** — 200,000 rows

Each experiment was repeated **3 times**, and the average was calculated.

### Benchmark Results

| Dataset | Rows | Avg. Load Time | Avg. Processing Time | Avg. Total Time | Table Size |
|---|---:|---:|---:|---:|---:|
| 25% | 50,000 | 5.0913 s | 0.0864 s | 5.1776 s | 10.63 MB |
| 50% | 100,000 | 9.5502 s | 0.1731 s | 9.7234 s | 21.23 MB |
| 100% | 200,000 | 18.7133 s | 0.3596 s | 19.0729 s | 42.43 MB |

The results show that both loading and processing time increase as the amount of data increases.

The PostgreSQL table size also grows approximately proportionally with the number of records.

### Database Size

The PostgreSQL database was measured using:

```sql
SELECT pg_size_pretty(pg_database_size('youtube'));
```

Measured database size:

```text
92 MB
```

### Container Memory

Observed Docker memory usage during execution:

```text
PostgreSQL: approximately 135–136 MiB
Loader:     approximately 275 MiB
```

The processor container completed quickly, so its memory usage was not captured reliably by `docker stats`.

### Benchmark Implementation

The benchmark is implemented in:

```text
src/benchmark.py
```

It:

1. loads 25%, 50% and 100% of the dataset;
2. measures loading time;
3. executes processing queries;
4. measures processing time;
5. calculates total execution time;
6. measures PostgreSQL table size;
7. repeats each experiment three times;
8. saves the results to `results/benchmark_results.csv`.

---

## 10. Processing Results

The six analytical queries generate CSV files in:

```text
results/
```

One complete pipeline execution produced the following processing times:

| Query | Time |
|---|---:|
| Country uniqueness | 0.9148 s |
| Music and gaming | 0.0423 s |
| Drama Score | 0.1219 s |
| Longest trending | 0.4395 s |
| Time to trend | 0.4117 s |
| Shouty titles | 7.1790 s |

The measurements demonstrate that different analytical queries have significantly different computational costs.

---

## 11. How to Run

### Requirements

- Docker
- Docker Compose
- Git

### Clone the Repository

```bash
git clone https://github.com/wowaid/cids_project_youtube.git
cd cids_project_youtube
```

### Start the Complete Pipeline

```bash
docker compose up --build
```

This command:

1. starts PostgreSQL;
2. waits until PostgreSQL is healthy;
3. downloads the dataset from GitHub;
4. loads the data into PostgreSQL;
5. runs the six SQL queries;
6. saves the results;
7. finishes the processing container.

### Stop the System

```bash
docker compose down
```

---

## 12. Reproducibility

The project is designed so that another user can reproduce the complete pipeline from the repository.

The system includes:

- a public input dataset;
- version-controlled source code;
- Dockerfiles;
- Docker Compose configuration;
- PostgreSQL database;
- automated data loading;
- SQL processing;
- saved results;
- benchmark measurements.

The complete system is started with:

```bash
docker compose up --build
```

The same command reproduces the main data pipeline without requiring a local PostgreSQL installation or manual database setup.

---

## 13. Repository

GitHub:

https://github.com/wowaid/cids_project_youtube