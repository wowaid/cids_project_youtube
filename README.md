# CIDS — YouTube Trending Video Statistics

This repository contains the public YouTube Trending Video Statistics dataset and the computing infrastructure used for a CIDS project.

The project builds a data pipeline for collecting, storing, processing and analysing YouTube Trending data across multiple countries using Docker, PostgreSQL, SQL and Python.

## Dataset

**Source:**  
Mitchell J. — *Trending YouTube Video Statistics, 2017–2018*

The dataset contains trending YouTube video statistics for 10 countries:

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

The data includes:

- video views
- likes
- dislikes
- comments
- title
- channel
- publication date
- trending date
- category
- country
- other video metadata

The original dataset is provided as country-specific CSV files together with category mapping JSON files.

## Project

The project focuses on building a reproducible computing infrastructure for loading, storing and querying a large public dataset.

The data pipeline uses:

**GitHub → Docker → PostgreSQL → SQL → Python → Interactive Dashboards**

The dataset is downloaded automatically from GitHub inside a Docker container and loaded into a PostgreSQL database. SQL queries are then used to aggregate and analyse the data, while Python is used to generate the final interactive dashboards.

## Research Questions

The dashboards will answer the following questions:

### 1. Which country has the most unique Trending chart?

Which country's trending videos overlap the least with the other nine countries?

The analysis will measure the proportion of videos that are unique to each country's Trending chart.

### 2. Which countries are the most music-obsessed and gaming-obsessed?

Which countries have the highest share of Trending videos belonging to:

- Music
- Gaming

Category share will be used rather than raw video counts to make countries comparable.

### 3. What is the most dramatic trending video?

Which video has the highest number of comments relative to its number of views?

The **Drama Score** is calculated as:

```text
DramaScore = (comment_count / views) × 1000
```

The analysis will identify the videos generating the highest number of comments per 1,000 views.

### 4. Which video refused to leave the Trending chart?

Which video stayed on the Trending chart for the longest period, and in how many countries did it trend?

Trending duration is calculated from the first to the last observed trending date.

### 5. How many days pass between publishing and trending?

How long does it take for a video to appear on the Trending chart after it is published?

The **Time to Trend** metric is calculated as:

```text
TimeToTrend = TrendingDate - PublishDate
```

The analysis will compare the distribution of this metric across countries.

### 6. Do shouty titles get more views?

Do videos with more expressive titles receive more views?

The analysis will investigate title characteristics such as:

- CAPITAL LETTERS
- exclamation marks (`!`)
- emojis

and compare them with video popularity.

## Data Structure

The original dataset contains one CSV file per country:

```text
CAvideos.csv
DEvideos.csv
FRvideos.csv
GBvideos.csv
INvideos.csv
JPvideos.csv
KRvideos.csv
MXvideos.csv
RUvideos.csv
USvideos.csv
```

Category mappings are provided as JSON files.

For the computing pipeline, the country datasets are combined into a compact dataset used by the Docker-based loading process.

## Computing Infrastructure

The project uses:

- **Docker / Docker Compose** — containerised infrastructure
- **PostgreSQL** — relational database
- **Python** — data processing and visualisation
- **Pandas** — data manipulation
- **SQLAlchemy** — database connection
- **Plotly** — interactive visualisations
- **GitHub** — dataset and project version control

The main database contains the combined YouTube trending data in a relational structure.

## Database

The PostgreSQL database contains:

### `videos`

Stores the main YouTube Trending records.

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

Stores the mapping between YouTube category IDs and category names.

```text
category_id
category_name
```

The two tables are joined using:

```text
videos.category_id = categories.category_id
```

## Project Structure

```text
cids_project_youtube/
│
├── data/
│   └── youtube_trending.csv
│
├── docker/
│   └── Dockerfile
│
├── src/
│   ├── load_data.py
│   ├── test_db.py
│   └── visualize.py
│
├── docker-compose.yml
├── create_dataset.py
├── README.md
└── .gitignore
```

## Original Source

The dataset was originally obtained from Kaggle:

Mitchell J. — *Trending YouTube Video Statistics, 2017–2018*.

This GitHub repository provides the dataset in a form suitable for the project's Docker-based data pipeline and computing infrastructure.