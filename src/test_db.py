from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "postgresql+psycopg2://youtube:youtube@localhost:5432/youtube"
)

query = """
SELECT
    country,
    COUNT(*) AS videos,
    ROUND(AVG(views)) AS avg_views
FROM videos
GROUP BY country
ORDER BY avg_views DESC;
"""

df = pd.read_sql(query, engine)

print(df)