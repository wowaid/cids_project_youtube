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
    v.country,
    c.category_name,
    COUNT(*) AS videos,
    ROUND(
        PERCENTILE_CONT(0.5)
        WITHIN GROUP (ORDER BY v.views)
    ) AS median_views
FROM videos v
JOIN categories c
    ON v.category_id = c.category_id
GROUP BY v.country, c.category_name
HAVING COUNT(*) >= 100
ORDER BY median_views DESC;
"""


# Get data from PostgreSQL
df = pd.read_sql(query, engine)

print(df.head(20))


# Create heatmap
fig = px.density_heatmap(
    df,
    x="country",
    y="category_name",
    z="median_views",
    title="Median Views by Country and YouTube Category",
    labels={
        "country": "Country",
        "category_name": "Category",
        "median_views": "Median Views"
    },
    text_auto=".2s"
)


# Improve layout
fig.update_layout(
    xaxis_title="Country",
    yaxis_title="YouTube Category",
    height=800
)


# Save chart
fig.write_html("category_heatmap.html")

print("Chart saved to category_heatmap.html")