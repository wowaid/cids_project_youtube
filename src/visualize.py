from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px


# Connect to PostgreSQL
engine = create_engine(
    "postgresql+psycopg2://youtube:youtube@localhost:5432/youtube"
)


# SQL query
query = """
SELECT
    country,
    COUNT(*) AS videos,
    ROUND(
        PERCENTILE_CONT(0.5)
        WITHIN GROUP (ORDER BY views)
    ) AS median_views
FROM videos
GROUP BY country
ORDER BY median_views DESC;
"""


# Get data from PostgreSQL
df = pd.read_sql(query, engine)

print(df)


# Create interactive chart
fig = px.bar(
    df,
    x="country",
    y="median_views",
    title="Median Views of Trending YouTube Videos by Country",
    labels={
        "country": "Country",
        "median_views": "Median Views"
    },
    text="median_views"
)

fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    yaxis_title="Median Views",
    xaxis_title="Country"
)


# Save chart
fig.write_html("median_views_by_country.html")

print("Chart saved to median_views_by_country.html")